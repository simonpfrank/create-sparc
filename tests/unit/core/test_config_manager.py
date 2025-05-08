import unittest
import tempfile
import shutil
import json
import os
from pathlib import Path

from create_sparc_py.core.config_manager import ConfigManager
from create_sparc_py.utils import fs_utils


class TestConfigManager(unittest.TestCase):
    """Test suite for the ConfigManager class."""

    def setUp(self):
        """Set up temporary directory for testing."""
        # Create temp directory for configuration
        self.temp_dir = tempfile.mkdtemp()
        self.config_dir = Path(self.temp_dir) / "config"
        fs_utils.create_dir(self.config_dir)

        # Initialize ConfigManager with the test config directory
        self.config_manager = ConfigManager(self.config_dir)

    def tearDown(self):
        """Clean up temporary directory."""
        shutil.rmtree(self.temp_dir)

    def test_init(self):
        """Test ConfigManager initialization."""
        # Test that config directory was created
        self.assertTrue(fs_utils.exists(self.config_dir))

        # Test that config file was created
        config_file = self.config_dir / "config.json"
        self.assertTrue(fs_utils.exists(config_file))

        # Test that default configuration was created
        config_content = json.loads(fs_utils.read_file(config_file))
        self.assertIn("templates_dir", config_content)
        self.assertIn("default_template", config_content)
        self.assertIn("version", config_content)

    def test_get(self):
        """Test getting configuration values."""
        # Test getting existing value
        default_template = self.config_manager.get("default_template")
        self.assertEqual("default", default_template)

        # Test getting non-existent value with default
        test_value = self.config_manager.get("non_existent", "test_default")
        self.assertEqual("test_default", test_value)

    def test_set(self):
        """Test setting configuration values."""
        # Test setting a new value
        self.config_manager.set("test_key", "test_value")
        self.assertEqual("test_value", self.config_manager.get("test_key"))

        # Test overwriting an existing value
        self.config_manager.set("default_template", "new_template")
        self.assertEqual("new_template", self.config_manager.get("default_template"))

        # Verify changes were saved to file
        config_file = self.config_dir / "config.json"
        config_content = json.loads(fs_utils.read_file(config_file))
        self.assertEqual("test_value", config_content["test_key"])
        self.assertEqual("new_template", config_content["default_template"])

    def test_update(self):
        """Test updating multiple configuration values."""
        # Test updating multiple values
        updates = {
            "test_key1": "test_value1",
            "test_key2": "test_value2",
            "default_template": "updated_template",
        }
        self.config_manager.update(updates)

        # Verify values were updated
        self.assertEqual("test_value1", self.config_manager.get("test_key1"))
        self.assertEqual("test_value2", self.config_manager.get("test_key2"))
        self.assertEqual(
            "updated_template", self.config_manager.get("default_template")
        )

        # Verify changes were saved to file
        config_file = self.config_dir / "config.json"
        config_content = json.loads(fs_utils.read_file(config_file))
        self.assertEqual("test_value1", config_content["test_key1"])
        self.assertEqual("test_value2", config_content["test_key2"])
        self.assertEqual("updated_template", config_content["default_template"])

    def test_reset(self):
        """Test resetting configuration to defaults."""
        # Set some custom values
        self.config_manager.set("test_key", "test_value")
        self.config_manager.set("default_template", "custom_template")

        # Reset to defaults
        self.config_manager.reset()

        # Verify values were reset
        self.assertIsNone(self.config_manager.get("test_key"))
        self.assertEqual("default", self.config_manager.get("default_template"))

        # Verify changes were saved to file
        config_file = self.config_dir / "config.json"
        config_content = json.loads(fs_utils.read_file(config_file))
        self.assertNotIn("test_key", config_content)
        self.assertEqual("default", config_content["default_template"])

    def test_get_templates_dir(self):
        """Test getting templates directory."""
        # Test default value
        templates_dir = self.config_manager.get_templates_dir()
        self.assertIsInstance(templates_dir, Path)

        # Test custom value
        custom_path = Path(self.temp_dir) / "custom_templates"
        self.config_manager.set("templates_dir", str(custom_path))
        templates_dir = self.config_manager.get_templates_dir()
        self.assertEqual(custom_path, templates_dir)

    def test_set_templates_dir(self):
        """Test setting templates directory."""
        custom_path = Path(self.temp_dir) / "custom_templates"
        self.config_manager.set_templates_dir(custom_path)

        # Verify value was set
        templates_dir = self.config_manager.get_templates_dir()
        self.assertEqual(custom_path, templates_dir)

        # Verify value was saved to file
        config_file = self.config_dir / "config.json"
        config_content = json.loads(fs_utils.read_file(config_file))
        self.assertEqual(str(custom_path), config_content["templates_dir"])

    def test_get_ai_settings(self):
        """Test getting AI settings."""
        # Test default value
        ai_settings = self.config_manager.get_ai_settings()
        self.assertIsInstance(ai_settings, dict)
        self.assertIn("model", ai_settings)
        self.assertIn("temperature", ai_settings)

    def test_get_default_template(self):
        """Test getting default template name."""
        # Test default value
        default_template = self.config_manager.get_default_template()
        self.assertEqual("default", default_template)

        # Test custom value
        self.config_manager.set("default_template", "custom_template")
        default_template = self.config_manager.get_default_template()
        self.assertEqual("custom_template", default_template)

    def test_set_default_template(self):
        """Test setting default template name."""
        self.config_manager.set_default_template("custom_template")

        # Verify value was set
        default_template = self.config_manager.get_default_template()
        self.assertEqual("custom_template", default_template)

        # Verify value was saved to file
        config_file = self.config_dir / "config.json"
        config_content = json.loads(fs_utils.read_file(config_file))
        self.assertEqual("custom_template", config_content["default_template"])

    def test_load_invalid_config(self):
        """Test loading invalid configuration file."""
        # Create an invalid config file
        config_file = self.config_dir / "config.json"
        fs_utils.write_file(config_file, "{invalid json")

        # Create a new ConfigManager to force loading the invalid file
        config_manager = ConfigManager(self.config_dir)

        # Verify that default configuration was used
        self.assertEqual("default", config_manager.get_default_template())
        self.assertIn("templates_dir", config_manager.config)
