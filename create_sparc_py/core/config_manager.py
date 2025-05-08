"""
Configuration management for create-sparc-py.

This module provides the ConfigManager class for loading, validating,
and saving configuration settings.

This project is a Python port of the original create-sparc Node.js tool created by
Reuven Cohen (https://github.com/ruvnet). The original project can be found at:
https://github.com/ruvnet/rUv-dev.
"""

import os
import json
from pathlib import Path
from typing import Dict, Any, Optional, List, Union

from create_sparc_py.utils import logger, fs_utils, path_utils


class ConfigManager:
    """
    Manages configuration settings for the application.

    This class handles loading, validating, and saving configuration
    settings, including user preferences and defaults.
    """

    def __init__(self, config_dir: Optional[Path] = None):
        """
        Initialize the ConfigManager.

        Args:
            config_dir: Directory containing configuration files. If None, uses
                       the user's home directory.
        """
        if config_dir is None:
            # Use the default config directory in the user's home
            self.config_dir = Path.home() / ".create-sparc-py"
        else:
            self.config_dir = Path(config_dir)

        self.config_file = self.config_dir / "config.json"
        self.default_config = {
            "templates_dir": str(Path(__file__).parent.parent / "templates"),
            "ai_provider": "openai",
            "ai_settings": {
                "model": "gpt-4",
                "temperature": 0.7,
                "max_tokens": 2000,
            },
            "default_template": "default",
            "version": "0.1.0",
        }

        # Ensure the config directory exists
        if not fs_utils.exists(self.config_dir):
            logger.info(f"Creating configuration directory: {self.config_dir}")
            fs_utils.create_dir(self.config_dir)

        # Load or create the config file
        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """
        Load configuration from the config file.

        Returns:
            Configuration dictionary
        """
        if not fs_utils.exists(self.config_file):
            logger.info(f"Creating default configuration file: {self.config_file}")
            self._save_config(self.default_config)
            return dict(self.default_config)

        try:
            config_str = fs_utils.read_file(self.config_file)
            config = json.loads(config_str)

            # Merge with defaults to ensure all keys are present
            merged_config = dict(self.default_config)
            merged_config.update(config)

            # Update the file if any defaults were missing
            if len(merged_config) > len(config):
                logger.info("Updating configuration with new default settings")
                self._save_config(merged_config)

            return merged_config
        except Exception as e:
            logger.error(f"Error loading configuration: {e}")
            logger.warning("Using default configuration")
            return dict(self.default_config)

    def _save_config(self, config: Dict[str, Any]) -> bool:
        """
        Save configuration to the config file.

        Args:
            config: Configuration dictionary to save

        Returns:
            True if successful, False otherwise
        """
        try:
            config_str = json.dumps(config, indent=2)
            fs_utils.write_file(self.config_file, config_str)
            return True
        except Exception as e:
            logger.error(f"Error saving configuration: {e}")
            return False

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value.

        Args:
            key: Configuration key
            default: Default value if key doesn't exist

        Returns:
            Configuration value or default
        """
        return self.config.get(key, default)

    def set(self, key: str, value: Any) -> bool:
        """
        Set a configuration value.

        Args:
            key: Configuration key
            value: Value to set

        Returns:
            True if successful, False otherwise
        """
        self.config[key] = value
        return self._save_config(self.config)

    def update(self, updates: Dict[str, Any]) -> bool:
        """
        Update multiple configuration values.

        Args:
            updates: Dictionary of updates

        Returns:
            True if successful, False otherwise
        """
        self.config.update(updates)
        return self._save_config(self.config)

    def reset(self) -> bool:
        """
        Reset configuration to defaults.

        Returns:
            True if successful, False otherwise
        """
        self.config = dict(self.default_config)
        return self._save_config(self.config)

    def get_templates_dir(self) -> Path:
        """
        Get the templates directory.

        Returns:
            Path to templates directory
        """
        templates_dir = self.get("templates_dir")
        return (
            Path(templates_dir)
            if templates_dir
            else Path(__file__).parent.parent / "templates"
        )

    def set_templates_dir(self, path: Union[str, Path]) -> bool:
        """
        Set the templates directory.

        Args:
            path: New templates directory path

        Returns:
            True if successful, False otherwise
        """
        return self.set("templates_dir", str(path))

    def get_ai_settings(self) -> Dict[str, Any]:
        """
        Get AI settings.

        Returns:
            AI settings dictionary
        """
        return self.get("ai_settings", {})

    def get_default_template(self) -> str:
        """
        Get the default template name.

        Returns:
            Default template name
        """
        return self.get("default_template", "default")

    def set_default_template(self, template_name: str) -> bool:
        """
        Set the default template name.

        Args:
            template_name: New default template name

        Returns:
            True if successful, False otherwise
        """
        return self.set("default_template", template_name)


# Create a singleton instance
config_manager = ConfigManager()

__all__ = ["ConfigManager", "config_manager"]
