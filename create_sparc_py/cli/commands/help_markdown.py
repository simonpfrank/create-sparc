import os
from pathlib import Path

HELP_DIR = Path(__file__).parent / "help"


def get_help_markdown(command: str) -> str:
    """
    Load the markdown help file for a given command.
    Args:
        command: The CLI command name (e.g., 'init', 'wizard')
    Returns:
        The markdown help content as a string, or a default message if not found.
    """
    help_file = HELP_DIR / f"{command}.md"
    if help_file.exists():
        return help_file.read_text()
    return f"No help available for command: {command}"
