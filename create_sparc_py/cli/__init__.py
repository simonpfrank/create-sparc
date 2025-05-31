"""
Command-line interface for create-sparc-py.

This module provides the command-line interface for create-sparc-py,
including argument parsing and command routing.

This project is a Python port of the original create-sparc Node.js tool created by
Reuven Cohen (https://github.com/ruvnet). The original project can be found at:
https://github.com/ruvnet/rUv-dev.
"""

import sys
import argparse
from typing import List, Dict, Any, Optional, Callable

from create_sparc_py.utils import logger


def run(argv: List[str]) -> int:
    """
    Run the CLI with the given arguments.

    Args:
        argv: Command-line arguments (typically sys.argv)

    Returns:
        Exit code (0 for success, non-zero for failure)
    """
    parser = _create_parser()
    args = parser.parse_args(argv[1:])  # Skip the program name

    # If no subcommand is provided, show help and exit
    if not hasattr(args, "func"):
        parser.print_help()
        return 0

    # Set log level if provided
    if hasattr(args, "verbose") and args.verbose:
        logger.set_level("verbose")
    elif hasattr(args, "debug") and args.debug:
        logger.set_level("debug")

    # Call the appropriate command handler
    try:
        return args.func(args)
    except Exception as e:
        logger.error(f"Error: {e}")
        if logger.get_level() == "debug":
            import traceback

            traceback.print_exc()
        return 1


def _create_parser() -> argparse.ArgumentParser:
    """
    Create the argument parser for the CLI.

    Returns:
        Configured argument parser
    """
    # Create the top-level parser
    parser = argparse.ArgumentParser(
        prog="create-sparc-py",
        description="Python scaffolding tool using the SPARC methodology",
        epilog="For more information, visit: https://github.com/yourusername/create-sparc-py",
    )

    # Add global options
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")

    parser.add_argument("--debug", action="store_true", help="Enable debug output")

    parser.add_argument("--version", action="version", version="%(prog)s 0.1.0")

    # Create subparsers for commands
    subparsers = parser.add_subparsers(
        title="commands",
        dest="command",
        help="Commands to run",
    )

    # Add subparsers for each command
    _add_init_parser(subparsers)
    _add_add_parser(subparsers)
    _add_help_parser(subparsers)
    _add_wizard_parser(subparsers)
    _add_mcp_parser(subparsers)
    _add_aigi_parser(subparsers)
    _add_minimal_parser(subparsers)

    return parser


def _add_init_parser(subparsers: argparse._SubParsersAction) -> None:
    """
    Add parser for the 'init' command.

    Args:
        subparsers: Subparsers object to add to
    """
    # Import lazily to avoid circular imports
    from create_sparc_py.cli.commands import init_command

    parser = subparsers.add_parser(
        "init",
        help="Initialize a new project using a template",
    )

    parser.add_argument("name", help="Name of the project to create")

    parser.add_argument(
        "-t",
        "--template",
        default="default",
        help="Template to use (default: 'default')",
    )

    parser.add_argument("-d", "--directory", help="Directory to create the project in (default: <name>)")

    parser.set_defaults(func=init_command)


def _add_add_parser(subparsers: argparse._SubParsersAction) -> None:
    """
    Add parser for the 'add' command.

    Args:
        subparsers: Subparsers object to add to
    """
    # Import lazily to avoid circular imports
    from create_sparc_py.cli.commands import add_command

    parser = subparsers.add_parser(
        "add",
        help="Add a component to an existing project",
    )

    parser.add_argument("component", help="Component to add")

    parser.add_argument("name", help="Name of the component")

    parser.add_argument(
        "-d",
        "--directory",
        help="Directory to add the component to (default: current directory)",
    )

    parser.set_defaults(func=add_command)


def _add_help_parser(subparsers: argparse._SubParsersAction) -> None:
    """
    Add parser for the 'help' command.

    Args:
        subparsers: Subparsers object to add to
    """
    # Import lazily to avoid circular imports
    from create_sparc_py.cli.commands import help_command

    parser = subparsers.add_parser(
        "help",
        help="Show help for a command",
    )

    parser.add_argument("command", nargs="?", help="Command to show help for")

    parser.set_defaults(func=help_command)


def _add_wizard_parser(subparsers: argparse._SubParsersAction) -> None:
    """
    Add parser for the 'wizard' command.

    Args:
        subparsers: Subparsers object to add to
    """
    # Import lazily to avoid circular imports
    from create_sparc_py.cli.commands import wizard_command

    parser = subparsers.add_parser(
        "wizard",
        help="Run the project creation wizard",
    )
    parser.add_argument(
        "wizard_args",
        nargs=argparse.REMAINDER,
        help="Arguments for the wizard subcommands (e.g., list, add, audit-security, etc.)",
    )
    parser.set_defaults(func=wizard_command)


def _add_mcp_parser(subparsers: argparse._SubParsersAction) -> None:
    """
    Add parser for the 'configure-mcp' command.

    Args:
        subparsers: Subparsers object to add to
    """
    # Import lazily to avoid circular imports
    from create_sparc_py.cli.commands import configure_mcp_command

    parser = subparsers.add_parser(
        "configure-mcp",
        help="Configure MCP settings",
    )

    parser.set_defaults(func=configure_mcp_command)


def _add_aigi_parser(subparsers: argparse._SubParsersAction) -> None:
    """
    Add parser for the 'aigi' command.

    Args:
        subparsers: Subparsers object to add to
    """
    # Import lazily to avoid circular imports
    from create_sparc_py.cli.commands import aigi_command

    parser = subparsers.add_parser(
        "aigi",
        help="Generate AI-powered implementation",
    )

    parser.add_argument("prompt", help="Prompt for AI code generation")

    parser.set_defaults(func=aigi_command)


def _add_minimal_parser(subparsers: argparse._SubParsersAction) -> None:
    """
    Add parser for the 'minimal' command.

    Args:
        subparsers: Subparsers object to add to
    """
    # Import lazily to avoid circular imports
    from create_sparc_py.cli.commands import minimal_command

    parser = subparsers.add_parser(
        "minimal",
        help="Create a minimal project",
    )

    parser.add_argument("name", help="Name of the project to create")

    parser.add_argument("-d", "--directory", help="Directory to create the project in (default: <name>)")

    parser.set_defaults(func=minimal_command)


__all__ = ["run"]
