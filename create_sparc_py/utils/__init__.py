"""
Shared utilities for create-sparc-py.

This module provides utility functions and classes that are used throughout
the create-sparc-py package, including logging, error handling, and file system
operations.

This project is a Python port of the original create-sparc Node.js tool created by
Reuven Cohen (https://github.com/ruvnet). The original project can be found at:
https://github.com/ruvnet/rUv-dev.
"""

import os
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Union, Any, Iterator

import colorama
from colorama import Fore, Style


# Initialize colorama for cross-platform colored terminal output
colorama.init(autoreset=True)


class Logger:
    """
    Logger utility for consistent logging with colored output.

    This class provides methods for logging messages at different levels
    (debug, verbose, info, success, warning, error) with appropriate
    coloring for better readability.
    """

    # Logging levels in order of verbosity
    LEVELS = {
        "debug": 0,
        "verbose": 1,
        "info": 2,
        "success": 2,
        "warning": 3,
        "error": 4,
    }

    def __init__(self) -> None:
        """Initialize the logger with default level of 'info'."""
        self._level = "info"

    def set_level(self, level: str) -> None:
        """
        Set the logging level.

        Args:
            level: Logging level (debug, verbose, info, warning, error)
        """
        if level not in self.LEVELS:
            raise ValueError(
                f"Invalid logging level: {level}. Valid levels are: {', '.join(self.LEVELS.keys())}"
            )
        self._level = level

    def get_level(self) -> str:
        """
        Get the current logging level.

        Returns:
            Current logging level
        """
        return self._level

    def _should_log(self, level: str) -> bool:
        """
        Check if a message at the given level should be logged.

        Args:
            level: Log level to check

        Returns:
            True if the message should be logged, False otherwise
        """
        return self.LEVELS[level] >= self.LEVELS[self._level]

    def debug(self, message: str) -> None:
        """
        Log a debug message (gray, only in debug mode).

        Args:
            message: Message to log
        """
        if self._should_log("debug"):
            print(f"{Fore.LIGHTBLACK_EX}[debug] {message}{Style.RESET_ALL}")

    def verbose(self, message: str) -> None:
        """
        Log a verbose message (blue, only in verbose or debug mode).

        Args:
            message: Message to log
        """
        if self._should_log("verbose"):
            print(f"{Fore.BLUE}[verbose] {message}{Style.RESET_ALL}")

    def info(self, message: str) -> None:
        """
        Log an info message (white).

        Args:
            message: Message to log
        """
        if self._should_log("info"):
            print(f"{Fore.WHITE}{message}{Style.RESET_ALL}")

    def success(self, message: str) -> None:
        """
        Log a success message (green).

        Args:
            message: Message to log
        """
        if self._should_log("info"):
            print(f"{Fore.GREEN}✓ {message}{Style.RESET_ALL}")

    def warning(self, message: str) -> None:
        """
        Log a warning message (yellow).

        Args:
            message: Message to log
        """
        if self._should_log("warning"):
            print(f"{Fore.YELLOW}⚠ {message}{Style.RESET_ALL}")

    def error(self, message: str) -> None:
        """
        Log an error message (red).

        Args:
            message: Message to log
        """
        if self._should_log("error"):
            print(f"{Fore.RED}✖ {message}{Style.RESET_ALL}")


class ErrorHandler:
    """
    Error handling utilities.

    This class provides methods for categorizing, formatting, and
    handling errors in a consistent way.
    """

    @staticmethod
    def categorize(error: Exception) -> Dict[str, Union[str, bool]]:
        """
        Categorize an error.

        Args:
            error: Error to categorize

        Returns:
            Dict with error category information
        """
        # File system errors
        if isinstance(error, FileNotFoundError):
            return {
                "type": "FILE_NOT_FOUND",
                "recoverable": False,
                "message": "File or directory not found",
            }

        if isinstance(error, PermissionError):
            return {
                "type": "PERMISSION_DENIED",
                "recoverable": False,
                "message": "Permission denied",
            }

        if isinstance(error, FileExistsError):
            return {
                "type": "FILE_EXISTS",
                "recoverable": True,
                "message": "File or directory already exists",
            }

        # Default
        return {"type": "UNKNOWN_ERROR", "recoverable": False, "message": str(error)}

    @staticmethod
    def format(error: Exception, verbose: bool = False) -> str:
        """
        Format an error for display.

        Args:
            error: Error to format
            verbose: Whether to include verbose details

        Returns:
            Formatted error message
        """
        category = ErrorHandler.categorize(error)
        message = f"{category['type']}: {category['message']}: {str(error)}"

        if verbose and hasattr(error, "__traceback__"):
            import traceback

            tb = "".join(
                traceback.format_exception(type(error), error, error.__traceback__)
            )
            message += f"\nTraceback (most recent call last):\n{tb}"

        return message


class FSUtils:
    """
    File system utilities for common file operations.

    This class provides methods for reading, writing, copying, and checking
    file system entities. It uses pathlib.Path for all operations.
    """

    @staticmethod
    def exists(path: Union[str, Path]) -> bool:
        """
        Check if a path exists.

        Args:
            path: Path to check

        Returns:
            True if the path exists, False otherwise
        """
        return Path(path).exists()

    @staticmethod
    def is_directory(path: Union[str, Path]) -> bool:
        """
        Check if a path is a directory.

        Args:
            path: Path to check

        Returns:
            True if the path is a directory, False otherwise
        """
        return Path(path).is_dir()

    @staticmethod
    def is_file(path: Union[str, Path]) -> bool:
        """
        Check if a path is a file.

        Args:
            path: Path to check

        Returns:
            True if the path is a file, False otherwise
        """
        return Path(path).is_file()

    @staticmethod
    def read_file(path: Union[str, Path], encoding: str = "utf-8") -> str:
        """
        Read the contents of a file.

        Args:
            path: Path to the file
            encoding: File encoding (default: utf-8)

        Returns:
            File contents as string

        Raises:
            FileNotFoundError: If the file does not exist
            PermissionError: If the file cannot be read
        """
        return Path(path).read_text(encoding=encoding)

    @staticmethod
    def write_file(
        path: Union[str, Path], content: str, encoding: str = "utf-8"
    ) -> None:
        """
        Write content to a file.

        Args:
            path: Path to the file
            content: Content to write
            encoding: File encoding (default: utf-8)

        Raises:
            PermissionError: If the file cannot be written
        """
        path = Path(path)

        # Create parent directories if they don't exist
        if not path.parent.exists():
            path.parent.mkdir(parents=True, exist_ok=True)

        path.write_text(content, encoding=encoding)

    @staticmethod
    def copy_file(src: Union[str, Path], dest: Union[str, Path]) -> None:
        """
        Copy a file from source to destination.

        Args:
            src: Source file path
            dest: Destination file path

        Raises:
            FileNotFoundError: If the source file does not exist
            PermissionError: If the file cannot be copied
        """
        src_path = Path(src)
        dest_path = Path(dest)

        # Create parent directories if they don't exist
        if not dest_path.parent.exists():
            dest_path.parent.mkdir(parents=True, exist_ok=True)

        shutil.copy2(src_path, dest_path)

    @staticmethod
    def copy_dir(src: Union[str, Path], dest: Union[str, Path]) -> None:
        """
        Copy a directory recursively from source to destination.

        Args:
            src: Source directory path
            dest: Destination directory path

        Raises:
            FileNotFoundError: If the source directory does not exist
            PermissionError: If the directory cannot be copied
        """
        src_path = Path(src)
        dest_path = Path(dest)

        if not src_path.exists():
            raise FileNotFoundError(f"Source directory does not exist: {src_path}")

        if not src_path.is_dir():
            raise NotADirectoryError(f"Source is not a directory: {src_path}")

        # Create destination directory if it doesn't exist
        dest_path.mkdir(parents=True, exist_ok=True)

        # Copy directory contents recursively
        shutil.copytree(src_path, dest_path, dirs_exist_ok=True)

    @staticmethod
    def create_dir(path: Union[str, Path], exist_ok: bool = True) -> None:
        """
        Create a directory.

        Args:
            path: Directory path
            exist_ok: Whether to ignore if directory already exists

        Raises:
            FileExistsError: If the directory already exists and exist_ok is False
            PermissionError: If the directory cannot be created
        """
        Path(path).mkdir(parents=True, exist_ok=exist_ok)

    @staticmethod
    def list_dir(path: Union[str, Path], pattern: Optional[str] = None) -> List[Path]:
        """
        List the contents of a directory.

        Args:
            path: Directory path
            pattern: Optional glob pattern to filter results

        Returns:
            List of paths in the directory

        Raises:
            FileNotFoundError: If the directory does not exist
            NotADirectoryError: If the path is not a directory
        """
        path_obj = Path(path)

        if not path_obj.exists():
            raise FileNotFoundError(f"Directory does not exist: {path}")

        if not path_obj.is_dir():
            raise NotADirectoryError(f"Not a directory: {path}")

        if pattern:
            return list(path_obj.glob(pattern))
        else:
            return list(path_obj.iterdir())

    @staticmethod
    def remove_file(path: Union[str, Path]) -> None:
        """
        Remove a file.

        Args:
            path: Path to the file

        Raises:
            FileNotFoundError: If the file does not exist
            PermissionError: If the file cannot be removed
        """
        Path(path).unlink()

    @staticmethod
    def remove_dir(path: Union[str, Path]) -> None:
        """
        Remove a directory and all its contents.

        Args:
            path: Path to the directory

        Raises:
            FileNotFoundError: If the directory does not exist
            PermissionError: If the directory cannot be removed
        """
        shutil.rmtree(Path(path))


class PathUtils:
    """
    Path manipulation utilities.

    This class provides methods for manipulating and working with paths.
    It uses pathlib.Path for all operations.
    """

    @staticmethod
    def resolve(path: Union[str, Path], *paths: Union[str, Path]) -> Path:
        """
        Resolve a path to its absolute form.

        Args:
            path: Base path
            *paths: Additional path components to join

        Returns:
            Resolved absolute path
        """
        return Path(path, *paths).resolve()

    @staticmethod
    def join(path: Union[str, Path], *paths: Union[str, Path]) -> Path:
        """
        Join path components.

        Args:
            path: Base path
            *paths: Additional path components to join

        Returns:
            Joined path
        """
        return Path(path, *paths)

    @staticmethod
    def is_absolute(path: Union[str, Path]) -> bool:
        """
        Check if a path is absolute.

        Args:
            path: Path to check

        Returns:
            True if the path is absolute, False otherwise
        """
        return Path(path).is_absolute()

    @staticmethod
    def get_relative_path(path: Union[str, Path], base: Union[str, Path]) -> Path:
        """
        Get path relative to a base directory.

        Args:
            path: Path to convert
            base: Base directory

        Returns:
            Path relative to base
        """
        return Path(path).relative_to(base)

    @staticmethod
    def get_name(path: Union[str, Path]) -> str:
        """
        Get the name component of a path.

        Args:
            path: Path to process

        Returns:
            Name component (final path component)
        """
        return Path(path).name

    @staticmethod
    def get_stem(path: Union[str, Path]) -> str:
        """
        Get the stem component of a path (filename without extension).

        Args:
            path: Path to process

        Returns:
            Stem component (filename without extension)
        """
        return Path(path).stem

    @staticmethod
    def get_suffix(path: Union[str, Path]) -> str:
        """
        Get the suffix component of a path (file extension).

        Args:
            path: Path to process

        Returns:
            Suffix component (file extension including the leading dot)
        """
        return Path(path).suffix

    @staticmethod
    def get_parent(path: Union[str, Path]) -> Path:
        """
        Get the parent directory of a path.

        Args:
            path: Path to process

        Returns:
            Parent directory
        """
        return Path(path).parent

    @staticmethod
    def change_extension(path: Union[str, Path], new_extension: str) -> Path:
        """
        Change the extension of a path.

        Args:
            path: Path to process
            new_extension: New extension (should include the leading dot)

        Returns:
            Path with new extension
        """
        path_obj = Path(path)
        if not new_extension.startswith(".") and new_extension:
            new_extension = f".{new_extension}"
        return path_obj.with_suffix(new_extension)


# Create singleton instances
logger = Logger()
error_handler = ErrorHandler()
fs_utils = FSUtils()
path_utils = PathUtils()


# Re-export for easier imports
__all__ = ["logger", "error_handler", "fs_utils", "path_utils"]


# File system utilities will be implemented next in a separate edit to keep this file manageable.
