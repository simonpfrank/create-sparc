"""
Core functionality for create-sparc-py.

This package contains the core functionality of create-sparc-py,
including template management, project generation, and configuration.

This project is a Python port of the original create-sparc Node.js tool created by
Reuven Cohen (https://github.com/ruvnet). The original project can be found at:
https://github.com/ruvnet/rUv-dev.
"""

from create_sparc_py.core.template_manager import TemplateManager, template_manager
from create_sparc_py.core.config_manager import ConfigManager, config_manager
from create_sparc_py.core.project_generator import ProjectGenerator, project_generator

__all__ = [
    "TemplateManager",
    "template_manager",
    "ConfigManager",
    "config_manager",
    "ProjectGenerator",
    "project_generator",
]
