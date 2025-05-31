"""
Project generation for create-sparc-py.

This module provides the ProjectGenerator class for generating new projects
using templates and configuration settings.

This project is a Python port of the original create-sparc Node.js tool created by
Reuven Cohen (https://github.com/ruvnet). The original project can be found at:
https://github.com/ruvnet/rUv-dev.
"""

import os
import json
from pathlib import Path
from typing import Dict, Any, Optional, List, Union

from create_sparc_py.utils import logger, fs_utils, path_utils
from create_sparc_py.core.template_manager import template_manager
from create_sparc_py.core.config_manager import config_manager


class ProjectGenerator:
    """
    Generates new projects using templates and configuration.

    This class orchestrates the creation of new projects, handling template
    application, configuration, and additional project setup.
    """

    def __init__(self):
        """Initialize the ProjectGenerator."""
        pass

    def generate_project(
        self,
        project_name: str,
        template_name: Optional[str] = None,
        output_dir: Optional[Union[str, Path]] = None,
        variables: Optional[Dict[str, Any]] = None,
    ) -> bool:
        """
        Generate a new project.

        Args:
            project_name: Name of the project to create
            template_name: Name of the template to use (defaults to configured default)
            output_dir: Directory to create the project in (defaults to project_name)
            variables: Additional template variables

        Returns:
            True if successful, False otherwise
        """
        try:
            # Set default template if not specified
            if template_name is None:
                template_name = config_manager.get_default_template()
                logger.info(f"Using default template: {template_name}")

            # Validate template existence
            available_templates = template_manager.list_templates()
            if not available_templates:
                logger.error("No templates available")
                return False

            if template_name not in available_templates:
                logger.error(f"Template '{template_name}' not found")
                logger.info(f"Available templates: {', '.join(available_templates)}")
                return False

            # Set default output directory if not specified
            if output_dir is None:
                output_dir = Path(project_name)
            else:
                output_dir = Path(output_dir)

            # Apply template
            logger.info(f"Generating project '{project_name}' using template '{template_name}'")
            success = template_manager.apply_template(template_name, project_name, output_dir)

            if not success:
                logger.error(f"Failed to generate project using template: {template_name}")
                return False

            # Additional project setup
            self._setup_additional_components(project_name, output_dir, variables)

            # Post-processing step
            self.post_process(project_name, output_dir, variables)

            return True

        except Exception as e:
            logger.error(f"Error generating project: {e}")
            if logger.get_level() == "debug":
                import traceback

                traceback.print_exc()
            return False

    def _setup_additional_components(
        self,
        project_name: str,
        output_dir: Path,
        variables: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Set up additional project components.

        Args:
            project_name: Name of the project
            output_dir: Project directory
            variables: Additional template variables
        """
        # This method can be expanded to add more project setup steps, such as:
        # - Setting up virtual environments
        # - Initializing git repositories
        # - Installing dependencies
        # - Additional SPARC-specific structure

        # For now, just log completion
        logger.info(f"Project '{project_name}' generated successfully in {output_dir}")

    def post_process(self, project_name: str, output_dir: Path, variables: Optional[Dict[str, Any]] = None) -> None:
        """
        Perform post-generation steps for the project (stub).

        Args:
            project_name: Name of the project
            output_dir: Project directory
            variables: Additional template variables
        """
        # TODO: Implement symlink creation, dependency installation, etc.
        logger.info(f"Post-processing for project '{project_name}' in {output_dir}")


# Create a singleton instance
project_generator = ProjectGenerator()

__all__ = ["ProjectGenerator", "project_generator"]
