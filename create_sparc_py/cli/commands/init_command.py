"""
'init' command implementation for create-sparc-py.

This module provides the implementation of the 'init' command, which
initializes a new project using a template.

This project is a Python port of the original create-sparc Node.js tool created by
Reuven Cohen (https://github.com/ruvnet). The original project can be found at:
https://github.com/ruvnet/rUv-dev.
"""

import argparse
import os
from pathlib import Path

from create_sparc_py.utils import logger
from create_sparc_py.core.project_generator import project_generator


def run(args: argparse.Namespace) -> int:
    """
    Run the 'init' command.

    Args:
        args: Command-line arguments

    Returns:
        Exit code (0 for success, non-zero for failure)
    """
    name = args.name
    template = args.template
    directory = args.directory

    logger.info(f"Initializing new project '{name}' using template '{template}'")

    # Use project_generator to generate the project
    success = project_generator.generate_project(
        project_name=name, template_name=template, output_dir=directory
    )

    if success:
        logger.success(f"Project '{name}' initialized successfully")
        return 0
    else:
        logger.error(f"Failed to initialize project '{name}'")
        return 1
