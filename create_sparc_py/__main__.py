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
import os
import traceback
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
    except ImportError as e:
        print(f"Import Error: {e}", file=sys.stderr)
        print("This usually means a command module is missing or has import issues.", file=sys.stderr)
        traceback.print_exc()
        return 1
    except AttributeError as e:
        print(f"Attribute Error: {e}", file=sys.stderr)
        print("This usually means a function is missing from a command module.", file=sys.stderr)
        traceback.print_exc()
        return 1
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(f"Error: {e}. {fname}, {exc_tb.tb_lineno}", file=sys.stderr)
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
