"""
Template management for create-sparc-py.

This module provides the TemplateManager class for loading, validating,
and applying templates for project generation.

This project is a Python port of the original create-sparc Node.js tool created by
Reuven Cohen (https://github.com/ruvnet). The original project can be found at:
https://github.com/ruvnet/rUv-dev.
"""

import os
import json
from pathlib import Path
from typing import Dict, Any, List, Optional

from create_sparc_py.utils import logger, fs_utils, path_utils


class TemplateManager:
    """
    Manages templates for project generation.

    This class handles loading templates, validating their structure,
    and applying them to generate new projects.
    """

    def __init__(self, templates_dir: Optional[Path] = None):
        """
        Initialize the TemplateManager.

        Args:
            templates_dir: Directory containing templates. If None, uses the default
                          templates directory in the package.
        """
        if templates_dir is None:
            # Import here to avoid circular imports
            from create_sparc_py.core.config_manager import config_manager

            self.templates_dir = config_manager.get_templates_dir()
        else:
            self.templates_dir = Path(templates_dir)

        # Ensure the templates directory exists
        if not fs_utils.exists(self.templates_dir):
            logger.warning(f"Templates directory not found: {self.templates_dir}")
            logger.info("Creating templates directory")
            fs_utils.create_dir(self.templates_dir)

    def list_templates(self) -> List[str]:
        """
        List available templates.

        Returns:
            List of template names
        """
        if not fs_utils.exists(self.templates_dir):
            return []

        # Only include directories that contain a template.json file
        templates = []
        for item in fs_utils.list_dir(self.templates_dir):
            template_json = item / "template.json"
            if fs_utils.is_directory(item) and fs_utils.exists(template_json):
                templates.append(path_utils.get_name(item))

        return templates

    def get_template_info(self, template_name: str) -> Dict[str, Any]:
        """
        Get information about a template.

        Args:
            template_name: Name of the template

        Returns:
            Template information as a dictionary

        Raises:
            FileNotFoundError: If the template or its configuration does not exist
        """
        template_dir = self.templates_dir / template_name
        template_json = template_dir / "template.json"

        if not fs_utils.exists(template_dir):
            raise FileNotFoundError(f"Template not found: {template_name}")

        if not fs_utils.exists(template_json):
            raise FileNotFoundError(f"Template configuration not found: {template_json}")

        try:
            template_info = json.loads(fs_utils.read_file(template_json))
            return template_info
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid template configuration: {e}")

    def validate_template(self, template_name: str) -> bool:
        """
        Validate a template's structure and configuration.

        Args:
            template_name: Name of the template

        Returns:
            True if the template is valid, False otherwise
        """
        try:
            template_info = self.get_template_info(template_name)

            # Check required fields
            required_fields = ["name", "version", "description", "files"]
            for field in required_fields:
                if field not in template_info:
                    logger.error(f"Template is missing required field: {field}")
                    return False

            # Only require 'files' directory if not listing files directly
            template_dir = self.templates_dir / template_name
            files_field = template_info["files"]
            files_dir = template_dir / "files"
            if isinstance(files_field, list):
                # Files are listed directly, no need for 'files' dir
                for rel_path in files_field:
                    file_path = template_dir / rel_path
                    if not fs_utils.exists(file_path):
                        logger.error(f"Template file not found: {file_path}")
                        return False
                return True
            else:
                # Fallback to old behavior
                if not fs_utils.exists(files_dir):
                    logger.error(f"Template files directory not found: {files_dir}")
                    return False
                return True
        except (FileNotFoundError, ValueError) as e:
            logger.error(str(e))
            return False

    def apply_template(self, template_name: str, project_name: str, output_dir: Path) -> bool:
        """
        Apply a template to generate a new project.

        Args:
            template_name: Name of the template
            project_name: Name of the new project
            output_dir: Directory to create the project in

        Returns:
            True if the template was applied successfully, False otherwise
        """
        try:
            # Validate the template
            if not self.validate_template(template_name):
                return False

            # Get template info
            template_info = self.get_template_info(template_name)

            # Create output directory if it doesn't exist
            if not fs_utils.exists(output_dir):
                logger.info(f"Creating output directory: {output_dir}")
                fs_utils.create_dir(output_dir)

            template_dir = self.templates_dir / template_name
            files_field = template_info["files"]
            if isinstance(files_field, list):
                # Copy each file listed in template.json
                for rel_path in files_field:
                    src = template_dir / rel_path
                    dest = output_dir / rel_path
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    fs_utils.copy_file(src, dest)
                # Apply template variables
                self._apply_template_variables(output_dir, project_name, template_info)
                return True
            else:
                # Fallback to old behavior
                files_dir = template_dir / "files"
                logger.info(f"Copying template files to: {output_dir}")
                self._copy_template_files(files_dir, output_dir, project_name, template_info)
                self._apply_template_variables(output_dir, project_name, template_info)
                return True
        except Exception as e:
            logger.error(f"Error applying template: {e}")
            if logger.get_level() == "debug":
                import traceback

                traceback.print_exc()
            return False

    def _copy_template_files(
        self,
        source_dir: Path,
        dest_dir: Path,
        project_name: str,
        template_info: Dict[str, Any],
    ) -> None:
        """
        Copy template files to the output directory.

        Args:
            source_dir: Source directory containing template files
            dest_dir: Destination directory for the new project
            project_name: Name of the new project
            template_info: Template information
        """
        # Copy all files and directories from source_dir to dest_dir
        for item in fs_utils.list_dir(source_dir):
            rel_path = path_utils.get_relative_path(item, source_dir)
            dest_path = dest_dir / rel_path

            if fs_utils.is_directory(item):
                fs_utils.create_dir(dest_path)
                self._copy_template_files(item, dest_path, project_name, template_info)
            elif fs_utils.is_file(item):
                # Process file name (replace variables)
                dest_path_str = str(dest_path)
                dest_path_str = dest_path_str.replace("{{project_name}}", project_name)
                dest_path = Path(dest_path_str)

                # Copy the file
                fs_utils.copy_file(item, dest_path)

    def _apply_template_variables(self, output_dir: Path, project_name: str, template_info: Dict[str, Any]) -> None:
        """
        Apply template variables to files in the output directory.

        Args:
            output_dir: Output directory containing the new project
            project_name: Name of the new project
            template_info: Template information
        """
        # Get variables to replace
        variables = {
            "{{project_name}}": project_name,
            "{{project_description}}": template_info.get("description", ""),
            "{{template_name}}": template_info.get("name", ""),
            "{{template_version}}": template_info.get("version", ""),
        }

        # Add custom variables from template.json
        if "variables" in template_info:
            for key, value in template_info["variables"].items():
                variables[f"{{{{{key}}}}}"] = value

        # Process text files
        text_extensions = [
            ".txt",
            ".md",
            ".py",
            ".js",
            ".html",
            ".css",
            ".json",
            ".yaml",
            ".yml",
        ]
        for root, _, files in os.walk(output_dir):
            for filename in files:
                file_path = Path(root) / filename
                if any(str(file_path).endswith(ext) for ext in text_extensions):
                    self._replace_variables_in_file(file_path, variables)

    def _replace_variables_in_file(self, file_path: Path, variables: Dict[str, str]) -> None:
        """
        Replace variables in a file.

        Args:
            file_path: Path to the file
            variables: Dictionary of variables to replace
        """
        try:
            content = fs_utils.read_file(file_path)

            # Replace variables
            for var, value in variables.items():
                content = content.replace(var, value)

            # Write updated content
            fs_utils.write_file(file_path, content)
        except Exception as e:
            logger.warning(f"Error processing variables in {file_path}: {e}")

    def render_template(self, template_str: str, context: dict) -> str:
        """
        Render a template string using Jinja2 with the provided context.

        Args:
            template_str: The template string to render
            context: Dictionary of variables for template rendering

        Returns:
            Rendered string
        """
        from jinja2 import Template

        template = Template(template_str)
        return template.render(**context)


# Create a singleton instance
template_manager = TemplateManager()

__all__ = ["TemplateManager", "template_manager"]
