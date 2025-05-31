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

        # Create template files in the template root (not in 'files/')
        readme_content = "# {{project_name}}\n\nBy {{author}}\n\n{{project_description}}"
        fs_utils.write_file(self.test_template_dir / "README.md", readme_content)

        index_content = """#!/usr/bin/env python
# {{project_name}}
# Version: {{template_version}}
# Description: {{project_description}}

def main():
    print("Hello from {{project_name}}")

if __name__ == "__main__":
    main()
"""
        fs_utils.write_file(self.test_template_dir / "index.py", index_content)

        # Create a file with project name in the filename
        config_content = '{"name": "{{project_name}}"}'
        fs_utils.write_file(self.test_template_dir / "{{project_name}}.json", config_content)
        self.template_json["files"].append("{{project_name}}.json")
        fs_utils.write_file(template_json_path, json.dumps(self.template_json))

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
        self.assertEqual(self.template_json["description"], template_info["description"])

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
        self.assertTrue(self.template_manager.validate_template(self.test_template_name))

        # Test with a template missing required fields
        missing_fields_template = "missing_fields_template"
        missing_fields_dir = self.templates_dir / missing_fields_template
        fs_utils.create_dir(missing_fields_dir)
        fs_utils.write_file(
            missing_fields_dir / "template.json",
            json.dumps({"name": "Missing Fields Template"}),
        )
        self.assertFalse(self.template_manager.validate_template(missing_fields_template))

        # Test with a template missing files directory (should be valid if files is an empty list)
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
        self.assertTrue(self.template_manager.validate_template(missing_files_template))

    def test_apply_template(self):
        """Test applying a template."""
        project_name = "test_project"
        project_dir = self.output_dir / project_name

        # Apply the template
        result = self.template_manager.apply_template(self.test_template_name, project_name, project_dir)
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
        result = self.template_manager.apply_template("non_existent", project_name, project_dir)
        self.assertFalse(result)

    def test_copy_template_files(self):
        """Test copying template files."""
        project_name = "test_copy"
        dest_dir = self.output_dir / project_name
        fs_utils.create_dir(dest_dir)
        variables = {
            "project_name": project_name,
            "project_description": self.template_json.get("description", ""),
            "template_name": self.template_json.get("name", ""),
            "template_version": self.template_json.get("version", ""),
            **self.template_json.get("variables", {}),
        }
        # Call the internal method directly
        self.template_manager._copy_template_files(
            self.test_template_dir, dest_dir, project_name, self.template_json, variables
        )
        # Check that files were copied
        self.assertTrue(fs_utils.exists(dest_dir / "README.md"))
        self.assertTrue(fs_utils.exists(dest_dir / "index.py"))
        self.assertTrue(fs_utils.exists(dest_dir / f"{project_name}.json"))

    def test_render_template(self):
        """Test the render_template method for variable substitution and logic."""
        manager = self.template_manager
        # Simple variable substitution
        template_str = "Hello, {{ name }}!"
        context = {"name": "World"}
        rendered = manager.render_template(template_str, context)
        self.assertEqual(rendered, "Hello, World!")

        # Conditional logic
        template_str = "{% if admin %}Admin{% else %}User{% endif %}"
        context = {"admin": True}
        rendered = manager.render_template(template_str, context)
        self.assertEqual(rendered, "Admin")
        context = {"admin": False}
        rendered = manager.render_template(template_str, context)
        self.assertEqual(rendered, "User")

        # Missing variable fallback (should return the original string due to StrictUndefined)
        template_str = "Hello, {{ missing_var }}!"
        context = {}
        rendered = manager.render_template(template_str, context)
        self.assertEqual(rendered, "Hello, {{ missing_var }}!")

    def test_apply_template_with_jinja2_logic(self):
        """Test applying a template with Jinja2 logic in files."""
        # Add a file with Jinja2 if/else and loop
        logic_content = """{% if admin %}Admin: {{ user }}{% else %}User: {{ user }}{% endif %}\n{% for i in range(2) %}Item {{ i }} {% endfor %}"""
        fs_utils.write_file(self.test_template_dir / "logic.md", logic_content)
        self.template_json["files"].append("logic.md")
        fs_utils.write_file(self.test_template_dir / "template.json", json.dumps(self.template_json))

        project_name = "jinja2_project"
        project_dir = self.output_dir / project_name
        result = self.template_manager.apply_template(
            self.test_template_name,
            project_name,
            project_dir,
            extra_vars={"admin": True, "user": "Alice", "range": range},
        )
        self.assertTrue(result)
        logic_out = fs_utils.read_file(project_dir / "logic.md")
        self.assertIn("Admin: Alice", logic_out)
        self.assertIn("Item 0", logic_out)
        self.assertIn("Item 1", logic_out)

    def test_apply_template_missing_required_variable(self):
        """Test that missing required variables cause apply_template to fail."""
        # Add required_variables to template.json
        self.template_json["required_variables"] = ["author", "license"]
        fs_utils.write_file(self.test_template_dir / "template.json", json.dumps(self.template_json))
        project_name = "missing_var"
        project_dir = self.output_dir / project_name
        # Should fail because 'license' is missing
        result = self.template_manager.apply_template(self.test_template_name, project_name, project_dir)
        self.assertFalse(result)
        # Should succeed if all required variables are provided
        result2 = self.template_manager.apply_template(
            self.test_template_name, project_name, project_dir, extra_vars={"license": "MIT"}
        )
        self.assertTrue(result2)

    def test_apply_template_with_nested_and_defaulted_variables(self):
        """Test template rendering with nested and defaulted variables."""
        nested_content = (
            "Project: {{ project.name | default('NoName') }}\nOwner: {{ owner.name if owner else 'None' }}"
        )
        fs_utils.write_file(self.test_template_dir / "nested.md", nested_content)
        self.template_json["files"].append("nested.md")
        fs_utils.write_file(self.test_template_dir / "template.json", json.dumps(self.template_json))
        project_name = "nested_project"
        project_dir = self.output_dir / project_name
        # Provide nested variables
        result = self.template_manager.apply_template(
            self.test_template_name,
            project_name,
            project_dir,
            extra_vars={"project": {"name": "Deep"}, "owner": {"name": "Bob"}},
        )
        self.assertTrue(result)
        nested_out = fs_utils.read_file(project_dir / "nested.md")
        self.assertIn("Project: Deep", nested_out)
        self.assertIn("Owner: Bob", nested_out)
        # Test default fallback
        result2 = self.template_manager.apply_template(
            self.test_template_name, project_name, project_dir, extra_vars={}
        )
        self.assertTrue(result2)
        nested_out2 = fs_utils.read_file(project_dir / "nested.md")
        self.assertIn("Project: NoName", nested_out2)
        self.assertIn("Owner: None", nested_out2)

    def test_apply_template_with_invalid_jinja2_syntax(self):
        """Test that invalid Jinja2 syntax in a template file does not crash apply_template."""
        bad_content = "{{ this is not valid jinja2 }}"
        fs_utils.write_file(self.test_template_dir / "bad.md", bad_content)
        self.template_json["files"].append("bad.md")
        fs_utils.write_file(self.test_template_dir / "template.json", json.dumps(self.template_json))
        project_name = "bad_jinja"
        project_dir = self.output_dir / project_name
        # Should not raise, but file will be copied as-is
        result = self.template_manager.apply_template(self.test_template_name, project_name, project_dir)
        self.assertTrue(result)
        bad_out = fs_utils.read_file(project_dir / "bad.md")
        self.assertIn("not valid jinja2", bad_out)

    def test_apply_template_with_empty_file(self):
        """Test that empty files are handled gracefully."""
        fs_utils.write_file(self.test_template_dir / "empty.txt", "")
        self.template_json["files"].append("empty.txt")
        fs_utils.write_file(self.test_template_dir / "template.json", json.dumps(self.template_json))
        project_name = "empty_file"
        project_dir = self.output_dir / project_name
        result = self.template_manager.apply_template(self.test_template_name, project_name, project_dir)
        self.assertTrue(result)
        empty_out = fs_utils.read_file(project_dir / "empty.txt")
        self.assertEqual(empty_out, "")
