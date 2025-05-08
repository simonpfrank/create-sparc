import unittest
import tempfile
import shutil
import json
import os
from pathlib import Path

from create_sparc_py.core.template_manager import TemplateManager
from create_sparc_py.utils import fs_utils


class TestTemplateManager(unittest.TestCase):
    """Test suite for the TemplateManager class."""

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

        # Create a file with project name in the filename
        config_content = '{"name": "{{project_name}}"}'
        fs_utils.write_file(self.files_dir / "{{project_name}}.json", config_content)

        # Initialize TemplateManager with the test templates directory
        self.template_manager = TemplateManager(self.templates_dir)

    def tearDown(self):
        """Clean up temporary directories."""
        shutil.rmtree(self.temp_dir)

    def test_init(self):
        """Test TemplateManager initialization."""
        # Test with a non-existent templates directory
        non_existent_dir = Path(self.temp_dir) / "non_existent"
        manager = TemplateManager(non_existent_dir)
        self.assertTrue(fs_utils.exists(non_existent_dir))

    def test_list_templates(self):
        """Test listing available templates."""
        templates = self.template_manager.list_templates()
        self.assertIn(self.test_template_name, templates)

        # Test with an empty directory
        empty_dir = Path(self.temp_dir) / "empty"
        fs_utils.create_dir(empty_dir)
        empty_manager = TemplateManager(empty_dir)
        self.assertEqual([], empty_manager.list_templates())

    def test_get_template_info(self):
        """Test getting template information."""
        # Test with an existing template
        template_info = self.template_manager.get_template_info(self.test_template_name)
        self.assertEqual(self.template_json["name"], template_info["name"])
        self.assertEqual(self.template_json["version"], template_info["version"])
        self.assertEqual(
            self.template_json["description"], template_info["description"]
        )

        # Test with a non-existent template
        with self.assertRaises(FileNotFoundError):
            self.template_manager.get_template_info("non_existent")

        # Test with a template that doesn't have template.json
        invalid_template_dir = self.templates_dir / "invalid_template"
        fs_utils.create_dir(invalid_template_dir)
        with self.assertRaises(FileNotFoundError):
            self.template_manager.get_template_info("invalid_template")

        # Test with an invalid JSON file
        invalid_json_template = "invalid_json_template"
        invalid_json_dir = self.templates_dir / invalid_json_template
        fs_utils.create_dir(invalid_json_dir)
        fs_utils.write_file(invalid_json_dir / "template.json", "{invalid json")
        with self.assertRaises(ValueError):
            self.template_manager.get_template_info(invalid_json_template)

    def test_validate_template(self):
        """Test template validation."""
        # Test with a valid template
        self.assertTrue(
            self.template_manager.validate_template(self.test_template_name)
        )

        # Test with a template missing required fields
        missing_fields_template = "missing_fields_template"
        missing_fields_dir = self.templates_dir / missing_fields_template
        fs_utils.create_dir(missing_fields_dir)
        fs_utils.write_file(
            missing_fields_dir / "template.json",
            json.dumps({"name": "Missing Fields Template"}),
        )
        self.assertFalse(
            self.template_manager.validate_template(missing_fields_template)
        )

        # Test with a template missing files directory
        missing_files_template = "missing_files_template"
        missing_files_dir = self.templates_dir / missing_files_template
        fs_utils.create_dir(missing_files_dir)
        fs_utils.write_file(
            missing_files_dir / "template.json",
            json.dumps(
                {
                    "name": "Missing Files Template",
                    "version": "1.0.0",
                    "description": "Template with missing files directory",
                    "files": [],
                }
            ),
        )
        self.assertFalse(
            self.template_manager.validate_template(missing_files_template)
        )

    def test_apply_template(self):
        """Test applying a template."""
        project_name = "test_project"
        project_dir = self.output_dir / project_name

        # Apply the template
        result = self.template_manager.apply_template(
            self.test_template_name, project_name, project_dir
        )
        self.assertTrue(result)

        # Check that the output directory was created
        self.assertTrue(fs_utils.exists(project_dir))

        # Check that the template files were copied
        self.assertTrue(fs_utils.exists(project_dir / "README.md"))
        self.assertTrue(fs_utils.exists(project_dir / "index.py"))

        # Check that variables were replaced
        readme_content = fs_utils.read_file(project_dir / "README.md")
        self.assertIn(project_name, readme_content)
        self.assertIn(self.template_json["variables"]["author"], readme_content)

        index_content = fs_utils.read_file(project_dir / "index.py")
        self.assertIn(project_name, index_content)
        self.assertIn(self.template_json["version"], index_content)

        # Check that filenames with variables were processed
        self.assertTrue(fs_utils.exists(project_dir / f"{project_name}.json"))
        config_content = fs_utils.read_file(project_dir / f"{project_name}.json")
        self.assertIn(project_name, config_content)

        # Test with a non-existent template
        result = self.template_manager.apply_template(
            "non_existent", project_name, project_dir
        )
        self.assertFalse(result)

    def test_copy_template_files(self):
        """Test copying template files."""
        project_name = "test_copy"
        dest_dir = self.output_dir / project_name
        fs_utils.create_dir(dest_dir)

        # Call the internal method directly
        self.template_manager._copy_template_files(
            self.files_dir, dest_dir, project_name, self.template_json
        )

        # Check that files were copied
        self.assertTrue(fs_utils.exists(dest_dir / "README.md"))
        self.assertTrue(fs_utils.exists(dest_dir / "index.py"))
        self.assertTrue(fs_utils.exists(dest_dir / f"{project_name}.json"))

    def test_apply_template_variables(self):
        """Test applying template variables to files."""
        project_name = "test_variables"
        dest_dir = self.output_dir / project_name
        fs_utils.create_dir(dest_dir)

        # Copy some files to the destination directory
        fs_utils.write_file(
            dest_dir / "test.txt", "Project: {{project_name}}, Author: {{author}}"
        )
        fs_utils.write_file(dest_dir / "test.py", "# {{project_description}}")

        # Apply variables
        self.template_manager._apply_template_variables(
            dest_dir, project_name, self.template_json
        )

        # Check that variables were replaced
        txt_content = fs_utils.read_file(dest_dir / "test.txt")
        self.assertIn(project_name, txt_content)
        self.assertIn(self.template_json["variables"]["author"], txt_content)

        py_content = fs_utils.read_file(dest_dir / "test.py")
        self.assertIn(self.template_json["description"], py_content)

    def test_replace_variables_in_file(self):
        """Test replacing variables in a file."""
        test_file = self.output_dir / "test_replace.txt"
        content = "Project: {{project_name}}, Version: {{template_version}}"
        fs_utils.write_file(test_file, content)

        variables = {
            "{{project_name}}": "test_project",
            "{{template_version}}": "1.0.0",
        }

        # Replace variables
        self.template_manager._replace_variables_in_file(test_file, variables)

        # Check the content
        replaced_content = fs_utils.read_file(test_file)
        self.assertEqual("Project: test_project, Version: 1.0.0", replaced_content)

        # Test with a non-existent file (should not raise exception)
        non_existent = self.output_dir / "non_existent.txt"
        self.template_manager._replace_variables_in_file(non_existent, variables)
