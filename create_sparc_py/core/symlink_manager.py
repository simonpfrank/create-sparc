import os
import sys
from pathlib import Path
from typing import Union


class SymlinkManager:
    """
    Handle symbolic link operations in a cross-platform way.
    """

    @staticmethod
    def create(target: Union[str, Path], link_name: Union[str, Path]) -> None:
        """
        Create a symbolic link pointing to target named link_name.
        Raises FileExistsError if link_name already exists.
        """
        target = str(target)
        link_name = str(link_name)
        try:
            if os.path.lexists(link_name):
                os.remove(link_name)
            os.symlink(target, link_name)
        except OSError as e:
            raise RuntimeError(f"Failed to create symlink: {e}")

    @staticmethod
    def exists(link_name: Union[str, Path]) -> bool:
        """
        Check if a symbolic link exists at link_name.
        """
        link_name = str(link_name)
        return os.path.islink(link_name)

    @staticmethod
    def is_symlink(path: Union[str, Path]) -> bool:
        """
        Check if the given path is a symbolic link.
        """
        path = str(path)
        return os.path.islink(path)

    @staticmethod
    def remove(link_name: Union[str, Path]) -> None:
        """
        Remove a symbolic link at link_name. Raises FileNotFoundError if not a symlink.
        """
        link_name = str(link_name)
        try:
            if os.path.islink(link_name) or os.path.exists(link_name):
                os.remove(link_name)
        except OSError as e:
            raise RuntimeError(f"Failed to remove symlink: {e}")

    @staticmethod
    def readlink(link_name: Union[str, Path]) -> str:
        """
        Return the target of the symbolic link at link_name.
        Raises FileNotFoundError if not a symlink.
        """
        link_name = str(link_name)
        try:
            return os.readlink(link_name)
        except OSError as e:
            raise RuntimeError(f"Failed to read symlink: {e}")
