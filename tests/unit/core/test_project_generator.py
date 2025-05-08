import unittest
import tempfile
import shutil
import json
import os
from pathlib import Path
from unittest.mock import patch, MagicMock

from create_sparc_py.core.project_generator import ProjectGenerator
from create_sparc_py.utils import fs_utils


class TestProjectGenerator(unittest.TestCase):
    """Test suite for the ProjectGenerator class."""

    def setUp(self):
        """Set up temporary directories for testing."""
        # Create temp directory for templates
        self.temp_dir = tempfile.mkdtemp()
        self.templates_dir = Path(self.temp_dir) / "templates"
        fs_utils.create_dir(self.templates_dir)

        # Create temp directory for output
        self.output_dir = Path(self.temp_dir) / "output"
        fs_utils.create_dir(self.output_dir)

        # Create a test template
        self.test_template_name = "test_template"
        self.test_template_dir = self.templates_dir / self.test_template_name
        fs_utils.create_dir(self.test_template_dir)

        # Create template.json
        self.template_json = {
            "name": "Test Template",
            "version": "1.0.0",
            "description": "A test template",
            "files": ["index.py", "README.md"],
            "variables": {"author": "Test Author"},
        }
        template_json_path = self.test_template_dir / "template.json"
        fs_utils.write_file(template_json_path, json.dumps(self.template_json))

        # Create template files directory
        self.files_dir = self.test_template_dir / "files"
        fs_utils.create_dir(self.files_dir)

        # Create some template files
        readme_content = (
            "# {{project_name}}\n\nBy {{author}}\n\n{{project_description}}"
        )
        fs_utils.write_file(self.files_dir / "README.md", readme_content)

        index_content = """#!/usr/bin/env python
# {{project_name}}
# Version: {{template_version}}
# Description: {{project_description}}

def main():
    print("Hello from {{project_name}}")

if __name__ == "__main__":
    main()
"""
        fs_utils.write_file(self.files_dir / "index.py", index_content)

        # Initialize ProjectGenerator
        self.project_generator = ProjectGenerator()

    def tearDown(self):
        """Clean up temporary directories."""
        shutil.rmtree(self.temp_dir)

    @patch("create_sparc_py.core.project_generator.template_manager")
    @patch("create_sparc_py.core.project_generator.config_manager")
    def test_generate_project(self, mock_config_manager, mock_template_manager):
        """Test project generation with default settings."""
        # Configure mocks
        mock_config_manager.get_default_template.return_value = "default"
        mock_template_manager.list_templates.return_value = ["default", "test_template"]
        mock_template_manager.apply_template.return_value = True

        # Generate project
        project_name = "test_project"
        result = self.project_generator.generate_project(
            project_name=project_name,
            template_name="default",
            output_dir=self.output_dir,
        )

        # Assert results
        self.assertTrue(result)
        mock_template_manager.apply_template.assert_called_once_with(
            "default", project_name, Path(self.output_dir)
        )

    @patch("create_sparc_py.core.project_generator.template_manager")
    @patch("create_sparc_py.core.project_generator.config_manager")
    def test_generate_project_with_default_template(
        self, mock_config_manager, mock_template_manager
    ):
        """Test project generation using the default template from config."""
        # Configure mocks
        mock_config_manager.get_default_template.return_value = "default"
        mock_template_manager.list_templates.return_value = ["default"]
        mock_template_manager.apply_template.return_value = True

        # Generate project without specifying template
        project_name = "test_project"
        result = self.project_generator.generate_project(
            project_name=project_name, output_dir=self.output_dir
        )

        # Assert results
        self.assertTrue(result)
        self.assertEqual(1, mock_config_manager.get_default_template.call_count)
        mock_template_manager.apply_template.assert_called_once_with(
            "default", project_name, Path(self.output_dir)
        )

    @patch("create_sparc_py.core.project_generator.template_manager")
    @patch("create_sparc_py.core.project_generator.config_manager")
    def test_generate_project_with_default_output_dir(
        self, mock_config_manager, mock_template_manager
    ):
        """Test project generation with default output directory."""
        # Configure mocks
        mock_config_manager.get_default_template.return_value = "default"
        mock_template_manager.list_templates.return_value = ["default"]
        mock_template_manager.apply_template.return_value = True

        # Generate project without specifying output directory
        project_name = "test_project"
        result = self.project_generator.generate_project(project_name=project_name)

        # Assert results
        self.assertTrue(result)
        mock_template_manager.apply_template.assert_called_once_with(
            "default", project_name, Path(project_name)
        )

    @patch("create_sparc_py.core.project_generator.template_manager")
    @patch("create_sparc_py.core.project_generator.config_manager")
    def test_generate_project_no_templates(
        self, mock_config_manager, mock_template_manager
    ):
        """Test project generation when no templates are available."""
        # Configure mocks
        mock_template_manager.list_templates.return_value = []

        # Attempt to generate project
        result = self.project_generator.generate_project(project_name="test_project")

        # Assert results
        self.assertFalse(result)
        mock_template_manager.apply_template.assert_not_called()

    @patch("create_sparc_py.core.project_generator.template_manager")
    @patch("create_sparc_py.core.project_generator.config_manager")
    def test_generate_project_template_not_found(
        self, mock_config_manager, mock_template_manager
    ):
        """Test project generation with non-existent template."""
        # Configure mocks
        mock_template_manager.list_templates.return_value = ["default"]

        # Attempt to generate project with non-existent template
        result = self.project_generator.generate_project(
            project_name="test_project", template_name="non_existent"
        )

        # Assert results
        self.assertFalse(result)
        mock_template_manager.apply_template.assert_not_called()

    @patch("create_sparc_py.core.project_generator.template_manager")
    @patch("create_sparc_py.core.project_generator.config_manager")
    def test_generate_project_template_error(
        self, mock_config_manager, mock_template_manager
    ):
        """Test project generation when template application fails."""
        # Configure mocks
        mock_config_manager.get_default_template.return_value = "default"
        mock_template_manager.list_templates.return_value = ["default"]
        mock_template_manager.apply_template.return_value = False

        # Attempt to generate project
        result = self.project_generator.generate_project(project_name="test_project")

        # Assert results
        self.assertFalse(result)
        mock_template_manager.apply_template.assert_called_once()

    @patch("create_sparc_py.core.project_generator.template_manager")
    @patch("create_sparc_py.core.project_generator.config_manager")
    def test_setup_additional_components(
        self, mock_config_manager, mock_template_manager
    ):
        """Test setup of additional components."""
        # For now, this method doesn't do much, so just test that it doesn't raise exceptions
        project_name = "test_project"
        output_dir = Path(self.temp_dir) / project_name
        fs_utils.create_dir(output_dir)

        # Configure mocks for generate_project call
        mock_config_manager.get_default_template.return_value = "default"
        mock_template_manager.list_templates.return_value = ["default"]
        mock_template_manager.apply_template.return_value = True

        # Call generate_project which should call _setup_additional_components
        result = self.project_generator.generate_project(
            project_name=project_name, output_dir=output_dir
        )

        # Assert results
        self.assertTrue(result)
        mock_template_manager.apply_template.assert_called_once()
