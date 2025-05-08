#!/usr/bin/env python3
"""
Main entry point for create-sparc-py CLI.

This module serves as the entry point for the create-sparc-py command-line tool.
It parses command-line arguments and routes them to the appropriate handlers.

This project is a Python port of the original create-sparc Node.js tool created by
Reuven Cohen (https://github.com/ruvnet). The original project can be found at:
https://github.com/ruvnet/rUv-dev.
"""

import sys
from create_sparc_py.cli import run


def main() -> int:
    """
    Main entry point for the create-sparc-py CLI.

    Returns:
        int: Exit code (0 for success, non-zero for failure)
    """
    try:
        return run(sys.argv)
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        return 1
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
