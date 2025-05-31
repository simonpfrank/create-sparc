import os
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
        target = Path(target)
        link_name = Path(link_name)
        if link_name.exists() or link_name.is_symlink():
            raise FileExistsError(f"Link already exists: {link_name}")
        link_name.parent.mkdir(parents=True, exist_ok=True)
        link_name.symlink_to(target, target_is_directory=target.is_dir())

    @staticmethod
    def exists(link_name: Union[str, Path]) -> bool:
        """
        Check if a symbolic link exists at link_name.
        """
        link_name = Path(link_name)
        return link_name.is_symlink()

    @staticmethod
    def is_symlink(path: Union[str, Path]) -> bool:
        """
        Check if the given path is a symbolic link.
        """
        return Path(path).is_symlink()

    @staticmethod
    def remove(link_name: Union[str, Path]) -> None:
        """
        Remove a symbolic link at link_name. Raises FileNotFoundError if not a symlink.
        """
        link_name = Path(link_name)
        if not link_name.is_symlink():
            raise FileNotFoundError(f"No symlink at: {link_name}")
        link_name.unlink()

    @staticmethod
    def readlink(link_name: Union[str, Path]) -> Path:
        """
        Return the target of the symbolic link at link_name.
        Raises FileNotFoundError if not a symlink.
        """
        link_name = Path(link_name)
        if not link_name.is_symlink():
            raise FileNotFoundError(f"No symlink at: {link_name}")
        return link_name.resolve()
