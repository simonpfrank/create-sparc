import os
import sys
import pytest
from pathlib import Path
from create_sparc_py.core.symlink_manager import SymlinkManager


def symlink_supported():
    # On Windows, symlink creation may require admin rights
    if os.name == "nt":
        import ctypes

        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    return True


@pytest.mark.skipif(not symlink_supported(), reason="Symlinks not supported or no admin rights.")
def test_create_and_exists_symlink(tmp_path):
    target = tmp_path / "target.txt"
    target.write_text("hello")
    link = tmp_path / "link.txt"
    SymlinkManager.create(target, link)
    assert link.exists()
    assert SymlinkManager.exists(link)
    assert SymlinkManager.is_symlink(link)
    assert link.resolve() == target.resolve()


@pytest.mark.skipif(not symlink_supported(), reason="Symlinks not supported or no admin rights.")
def test_create_symlink_to_dir(tmp_path):
    target_dir = tmp_path / "dir"
    target_dir.mkdir()
    link = tmp_path / "dir_link"
    SymlinkManager.create(target_dir, link)
    assert link.exists()
    assert SymlinkManager.exists(link)
    assert SymlinkManager.is_symlink(link)
    assert link.resolve() == target_dir.resolve()


@pytest.mark.skipif(not symlink_supported(), reason="Symlinks not supported or no admin rights.")
def test_create_symlink_already_exists(tmp_path):
    target = tmp_path / "target.txt"
    target.write_text("data")
    link = tmp_path / "link.txt"
    SymlinkManager.create(target, link)
    with pytest.raises(FileExistsError):
        SymlinkManager.create(target, link)
