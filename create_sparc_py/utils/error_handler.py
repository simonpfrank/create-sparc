from typing import Any


class ErrorHandler:
    """Error handling utilities."""

    @staticmethod
    def categorize(error: Exception) -> str:
        if hasattr(error, "errno"):
            return f"OS error {error.errno}"
        return error.__class__.__name__

    @staticmethod
    def format(error: Exception, verbose: bool = False) -> str:
        if verbose:
            import traceback

            return f"{error}\n{traceback.format_exc()}"
        return str(error)
