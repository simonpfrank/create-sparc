"""
Minimal command implementation for create-sparc-py.
"""

import argparse
from typing import Any, Dict, Optional
from create_sparc_py.utils import logger
from create_sparc_py.core.project_generator import project_generator


def run(args: Any) -> int:
    """
    Run the minimal command to create a minimal Roo project.

    Args:
        args: Parsed command-line arguments.

    Returns:
        Exit code (0 for success, non-zero for failure).
    """
    name = getattr(args, "name", None)
    directory = getattr(args, "directory", None)
    if not name:
        logger.error("Project name is required for minimal command.")
        return 1
    logger.info(f"Creating minimal Roo project '{name}' using minimal_roo template.")
    success = project_generator.generate_project(
        project_name=name,
        template_name="minimal_roo",
        output_dir=directory,
    )
    if success:
        logger.success(f"Minimal Roo project '{name}' created successfully.")
        return 0
    else:
        logger.error(f"Failed to create minimal Roo project '{name}'.")
        return 1
