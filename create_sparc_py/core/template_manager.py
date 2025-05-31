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
from jinja2 import Environment, FileSystemLoader, StrictUndefined, TemplateError
import shutil
import re

from create_sparc_py.utils import logger, fs_utils, path_utils


def _sanitize_context(obj):
    if isinstance(obj, dict):
        return {k: _sanitize_context(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [_sanitize_context(v) for v in obj]
    elif isinstance(obj, Path):
        return str(obj)
    else:
        return obj


class TemplateManager:
    """
    Manages templates for project generation.

    This class handles loading templates, validating their structure,
    and applying them to generate new projects.
    """

    def __init__(self, templates_dir: Optional[str] = None):
        """
        Initialize the TemplateManager.

        Args:
            templates_dir: Directory containing templates. If None, uses the default
                          templates directory in the package.
        """
        self.templates_dir = templates_dir or os.path.join(os.path.dirname(__file__), "../templates")
        self.env = Environment(
            loader=FileSystemLoader(self.templates_dir),
            undefined=StrictUndefined,
            keep_trailing_newline=True,
        )

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
        src_dir = os.path.join(self.templates_dir, template_name)
        info = {"name": template_name, "path": src_dir}
        yaml_path = os.path.join(src_dir, "template.yaml")
        if os.path.exists(yaml_path):
            import yaml

            with open(yaml_path, "r") as f:
                info.update(yaml.safe_load(f))
        return info

    def validate_template(self, template_name: str) -> Dict[str, Any]:
        """
        Validate a template's structure and configuration.

        Args:
            template_name: Name of the template

        Returns:
            Dictionary with 'valid' key indicating whether the template is valid
            and 'error' key if there's an error.
        """
        src_dir = os.path.join(self.templates_dir, template_name)
        if not os.path.isdir(src_dir):
            return {"valid": False, "error": f"Template directory not found: {src_dir}"}
        # Check for required files (e.g., template.yaml, README.md)
        required_files = ["template.yaml", "README.md"]
        missing = [f for f in required_files if not os.path.exists(os.path.join(src_dir, f))]
        if missing:
            return {"valid": False, "error": f"Missing required files: {', '.join(missing)}"}
        return {"valid": True}

    def apply_template(self, template_name: str, output_dir: str, context: Dict[str, Any]) -> None:
        """
        Apply a template to generate a new project.

        Args:
            template_name: Name of the template
            output_dir: Directory to create the project in
            context: Dictionary of variables to use in template rendering

        Raises:
            FileNotFoundError: If the template directory does not exist
        """
        context = _sanitize_context(context)
        if not isinstance(context, dict):
            raise TypeError("Template context must be a dict")
        src_dir = os.path.join(self.templates_dir, template_name)
        if not os.path.isdir(src_dir):
            raise FileNotFoundError(f"Template directory not found: {src_dir}")
        for root, dirs, files in os.walk(src_dir):
            rel_root = os.path.relpath(root, src_dir)
            for file in files:
                src_file = os.path.join(root, file)
                # Render filename as well as content, but only if context is a dict
                rendered_filename = file
                try:
                    rendered_filename = self.env.from_string(file).render(**context)
                except Exception:
                    rendered_filename = file
                dest_dir = os.path.join(output_dir, rel_root)
                os.makedirs(dest_dir, exist_ok=True)
                dest_file = os.path.join(dest_dir, rendered_filename)
                with open(src_file, "r") as f:
                    content = f.read()
                try:
                    rendered_content = self.env.from_string(content).render(**context)
                except Exception as e:
                    raise RuntimeError(f"Template rendering error in {src_file}: {e}")
                with open(dest_file, "w") as f:
                    f.write(rendered_content)

    def render_template(self, template_name: str, context: Dict[str, Any]) -> str:
        """
        Render a template string using Jinja2 with the provided context.
        """
        context = _sanitize_context(context)
        if not isinstance(context, dict):
            raise TypeError("Template context must be a dict")
        try:
            template = self.env.get_template(template_name)
            return template.render(**context)
        except TemplateError as e:
            raise RuntimeError(f"Template rendering error: {e}")


# Create a singleton instance
template_manager = TemplateManager()

__all__ = ["TemplateManager", "template_manager"]
