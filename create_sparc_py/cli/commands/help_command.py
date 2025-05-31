"""
Enhanced implementation for the help command.
"""

import argparse
from typing import Any
from create_sparc_py.cli import _create_parser
from .help_markdown import get_help_markdown
from rich.console import Console
from rich.markdown import Markdown


def run(args: Any) -> int:
    """
    Run the help command.

    Args:
        args: Parsed command-line arguments.

    Returns:
        Exit code (0 for success, non-zero for failure).
    """
    parser = _create_parser()
    if getattr(args, "command", None):
        command = args.command
        # Try to print the markdown help for the command
        help_md = get_help_markdown(command)
        if not help_md.startswith("No help available"):
            console = Console()
            console.print(Markdown(help_md))
            return 0
        # Fallback to argparse help
        subparsers_action = None
        for action in parser._actions:
            if isinstance(action, argparse._SubParsersAction):
                subparsers_action = action
                break
        if subparsers_action and command in subparsers_action.choices:
            subparser = subparsers_action.choices[command]
            subparser.print_help()
            return 0
        else:
            print(f"Unknown command: {command}")
            return 1
    else:
        # Print the main help (list of commands)
        parser.print_help()
        return 0
