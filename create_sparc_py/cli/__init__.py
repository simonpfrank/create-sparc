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
from create_sparc_py.cli.commands.help_markdown import get_help_markdown
from rich.console import Console
from rich.markdown import Markdown
from create_sparc_py.cli.parser_factory import create_parser


def run(argv: List[str]) -> int:
    """
    Run the CLI with the given arguments.

    Args:
        argv: Command-line arguments (typically sys.argv)

    Returns:
        Exit code (0 for success, non-zero for failure)
    """
    parser = create_parser()
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


class MarkdownHelpParser(argparse.ArgumentParser):
    def __init__(self, *args, command_name=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.command_name = command_name

    def print_help(self, file=None):
        if self.command_name:
            help_md = get_help_markdown(self.command_name)
            if not help_md.startswith("No help available"):
                console = Console()
                console.print(Markdown(help_md))
                return
        super().print_help(file=file)


def _create_parser() -> argparse.ArgumentParser:
    """
    Create the argument parser for the CLI.

    Returns:
        Configured argument parser
    """
    # Create the top-level parser
    parser = MarkdownHelpParser(
        prog="create-sparc-py",
        description="Python scaffolding tool using the SPARC methodology",
        epilog="For more information, visit: https://github.com/yourusername/create-sparc-py",
        command_name=None,
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

    # Add subparsers for each command, using MarkdownHelpParser for each
    def add_subparser_with_markdown(name, help_text, add_args_fn):
        subparser = subparsers.add_parser(
            name,
            help=help_text,
            cls=MarkdownHelpParser,
            command_name=name,
        )
        add_args_fn(subparser)
        return subparser

    add_subparser_with_markdown("init", "Initialize a new project using a template", _add_init_args)
    add_subparser_with_markdown("add", "Add a component to an existing project", _add_add_args)
    add_subparser_with_markdown("help", "Show help for a command", _add_help_args)
    add_subparser_with_markdown("wizard", "Run the project creation wizard", _add_wizard_args)
    add_subparser_with_markdown("configure-mcp", "Configure Multi-Cloud Provider settings", _add_mcp_args)
    add_subparser_with_markdown("aigi", "AI-Guided Implementation commands", _add_aigi_args)
    add_subparser_with_markdown("minimal", "Create a minimal Roo mode framework", _add_minimal_args)
    add_subparser_with_markdown("registry", "Registry client commands", _add_registry_args)

    return parser


def _add_init_args(parser):
    from create_sparc_py.cli.commands import init_command

    parser.add_argument("name", help="Name of the project to create")
    parser.add_argument(
        "-t",
        "--template",
        default="default",
        help="Template to use (default: 'default')",
    )
    parser.add_argument("-d", "--directory", help="Directory to create the project in (default: <name>)")
    parser.set_defaults(func=init_command)


def _add_add_args(parser):
    from create_sparc_py.cli.commands import add_command

    parser.add_argument("component", help="Component to add")
    parser.add_argument("name", help="Name of the component")
    parser.add_argument(
        "-d",
        "--directory",
        help="Directory to add the component to (default: current directory)",
    )
    parser.set_defaults(func=add_command)


def _add_help_args(parser):
    from create_sparc_py.cli.commands import help_command

    parser.add_argument("command", nargs="?", help="Command to show help for")
    parser.set_defaults(func=help_command)


def _add_wizard_args(parser):
    from create_sparc_py.cli.commands import wizard_command

    parser.add_argument(
        "wizard_args",
        nargs=argparse.REMAINDER,
        help="Arguments for the wizard subcommands (e.g., list, add, audit-security, etc.)",
    )
    parser.set_defaults(func=wizard_command)


def _add_mcp_args(parser):
    from create_sparc_py.cli.commands import configure_mcp_command

    parser.add_argument(
        "mcp_args",
        nargs=argparse.REMAINDER,
        help="Arguments for the configure-mcp subcommands (e.g., add, remove, update, list, etc.)",
    )
    parser.set_defaults(func=configure_mcp_command)


def _add_aigi_args(parser):
    from create_sparc_py.cli.commands import aigi_command

    parser.add_argument(
        "aigi_args",
        nargs=argparse.REMAINDER,
        help="Arguments for the aigi subcommands (e.g., init, etc.)",
    )
    parser.set_defaults(func=aigi_command)


def _add_minimal_args(parser):
    from create_sparc_py.cli.commands import minimal_command

    parser.add_argument(
        "minimal_args",
        nargs=argparse.REMAINDER,
        help="Arguments for the minimal subcommands (e.g., init, etc.)",
    )
    parser.set_defaults(func=minimal_command)


def _add_registry_args(parser):
    from create_sparc_py.cli.commands import registry_command

    parser.add_argument(
        "registry_args",
        nargs=argparse.REMAINDER,
        help="Arguments for the registry subcommands (e.g., list, get, post, auth, etc.)",
    )
    parser.set_defaults(func=registry_command)


__all__ = ["run"]
