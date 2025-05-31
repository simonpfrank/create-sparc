"""Unit tests for FSUtils class."""

import os
import shutil
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

from create_sparc_py.utils import FSUtils


class TestFSUtils:
    """Tests for the FSUtils class."""

    def test_exists(self):
        """Test checking if a path exists."""
        with patch("pathlib.Path.exists") as mock_exists:
            # Test with path exists
            mock_exists.return_value = True
            assert FSUtils.exists("test/path") is True
            mock_exists.assert_called_once()

            # Test with path does not exist
            mock_exists.reset_mock()
            mock_exists.return_value = False
            assert FSUtils.exists("test/path") is False
            mock_exists.assert_called_once()

            # Test with Path object
            mock_exists.reset_mock()
            path_obj = Path("test/path")
            FSUtils.exists(path_obj)
            mock_exists.assert_called_once()

    def test_is_directory(self):
        """Test checking if a path is a directory."""
        with patch("pathlib.Path.is_dir") as mock_is_dir:
            # Test with path is directory
            mock_is_dir.return_value = True
            assert FSUtils.is_directory("test/path") is True
            mock_is_dir.assert_called_once()

            # Test with path is not directory
            mock_is_dir.reset_mock()
            mock_is_dir.return_value = False
            assert FSUtils.is_directory("test/path") is False
            mock_is_dir.assert_called_once()

            # Test with Path object
            mock_is_dir.reset_mock()
            path_obj = Path("test/path")
            FSUtils.is_directory(path_obj)
            mock_is_dir.assert_called_once()

    def test_is_file(self):
        """Test checking if a path is a file."""
        with patch("pathlib.Path.is_file") as mock_is_file:
            # Test with path is file
            mock_is_file.return_value = True
            assert FSUtils.is_file("test/path") is True
            mock_is_file.assert_called_once()

            # Test with path is not file
            mock_is_file.reset_mock()
            mock_is_file.return_value = False
            assert FSUtils.is_file("test/path") is False
            mock_is_file.assert_called_once()

            # Test with Path object
            mock_is_file.reset_mock()
            path_obj = Path("test/path")
            FSUtils.is_file(path_obj)
            mock_is_file.assert_called_once()

    def test_read_file(self):
        """Test reading a file."""
        with patch("pathlib.Path.read_text") as mock_read_text:
            mock_read_text.return_value = "file content"

            # Test with default encoding
            content = FSUtils.read_file("test/file.txt")
            assert content == "file content"
            mock_read_text.assert_called_once_with(encoding="utf-8")

            # Test with custom encoding
            mock_read_text.reset_mock()
            content = FSUtils.read_file("test/file.txt", encoding="latin-1")
            assert content == "file content"
            mock_read_text.assert_called_once_with(encoding="latin-1")

            # Test with Path object
            mock_read_text.reset_mock()
            path_obj = Path("test/file.txt")
            FSUtils.read_file(path_obj)
            mock_read_text.assert_called_once_with(encoding="utf-8")

    def test_write_file(self):
        """Test writing to a file."""
        with patch("pathlib.Path.write_text") as mock_write_text, patch(
            "pathlib.Path.parent"
        ) as mock_parent, patch("pathlib.Path.exists") as mock_exists, patch(
            "pathlib.Path.mkdir"
        ) as mock_mkdir:

            # Set up mocks
            mock_exists.return_value = True

            # Test with parent exists
            FSUtils.write_file("test/file.txt", "content")
            mock_write_text.assert_called_once_with("content", encoding="utf-8")
            mock_mkdir.assert_not_called()

            # Test with parent does not exist
            mock_write_text.reset_mock()
            mock_exists.return_value = False

            FSUtils.write_file("test/file.txt", "content")
            mock_write_text.assert_called_once_with("content", encoding="utf-8")
            mock_mkdir.assert_called_once_with(parents=True, exist_ok=True)

            # Test with custom encoding
            mock_write_text.reset_mock()
            mock_mkdir.reset_mock()
            mock_exists.return_value = True

            FSUtils.write_file("test/file.txt", "content", encoding="latin-1")
            mock_write_text.assert_called_once_with("content", encoding="latin-1")

    def test_copy_file(self):
        """Test copying a file."""
        with patch("shutil.copy2") as mock_copy2, patch(
            "pathlib.Path.parent"
        ) as mock_parent, patch("pathlib.Path.exists") as mock_exists, patch(
            "pathlib.Path.mkdir"
        ) as mock_mkdir:

            # Set up mocks
            mock_exists.return_value = True

            # Test with parent exists
            FSUtils.copy_file("src/file.txt", "dest/file.txt")
            mock_copy2.assert_called_once()
            mock_mkdir.assert_not_called()

            # Test with parent does not exist
            mock_copy2.reset_mock()
            mock_exists.return_value = False

            FSUtils.copy_file("src/file.txt", "dest/file.txt")
            mock_copy2.assert_called_once()
            mock_mkdir.assert_called_once_with(parents=True, exist_ok=True)

            # Test with Path objects
            mock_copy2.reset_mock()
            mock_mkdir.reset_mock()

            src_path = Path("src/file.txt")
            dest_path = Path("dest/file.txt")
            FSUtils.copy_file(src_path, dest_path)
            mock_copy2.assert_called_once()

    def test_copy_dir(self):
        """Test copying a directory."""
        with patch("pathlib.Path.exists") as mock_exists, patch(
            "pathlib.Path.is_dir"
        ) as mock_is_dir, patch("pathlib.Path.mkdir") as mock_mkdir, patch(
            "shutil.copytree"
        ) as mock_copytree:

            # Set up mocks
            mock_exists.return_value = True
            mock_is_dir.return_value = True

            # Test copying directory
            FSUtils.copy_dir("src/dir", "dest/dir")
            mock_mkdir.assert_called_once_with(parents=True, exist_ok=True)
            mock_copytree.assert_called_once()

            # Test source does not exist
            mock_mkdir.reset_mock()
            mock_copytree.reset_mock()
            mock_exists.return_value = False

            with pytest.raises(FileNotFoundError):
                FSUtils.copy_dir("src/dir", "dest/dir")
            mock_mkdir.assert_not_called()
            mock_copytree.assert_not_called()

            # Test source is not a directory
            mock_exists.return_value = True
            mock_is_dir.return_value = False

            with pytest.raises(NotADirectoryError):
                FSUtils.copy_dir("src/dir", "dest/dir")
            mock_mkdir.assert_not_called()
            mock_copytree.assert_not_called()

    def test_create_dir(self):
        """Test creating a directory."""
        with patch("pathlib.Path.mkdir") as mock_mkdir:
            # Test with default exist_ok
            FSUtils.create_dir("test/dir")
            mock_mkdir.assert_called_once_with(parents=True, exist_ok=True)

            # Test with exist_ok=False
            mock_mkdir.reset_mock()
            FSUtils.create_dir("test/dir", exist_ok=False)
            mock_mkdir.assert_called_once_with(parents=True, exist_ok=False)

            # Test with Path object
            mock_mkdir.reset_mock()
            path_obj = Path("test/dir")
            FSUtils.create_dir(path_obj)
            mock_mkdir.assert_called_once_with(parents=True, exist_ok=True)

    def test_list_dir(self):
        """Test listing directory contents."""
        with patch("pathlib.Path.exists") as mock_exists, patch(
            "pathlib.Path.is_dir"
        ) as mock_is_dir, patch("pathlib.Path.iterdir") as mock_iterdir, patch(
            "pathlib.Path.glob"
        ) as mock_glob:

            # Set up mocks
            mock_exists.return_value = True
            mock_is_dir.return_value = True
            mock_items = [Path("file1.txt"), Path("file2.txt")]
            mock_iterdir.return_value = mock_items
            mock_glob.return_value = [Path("file1.txt")]

            # Test listing without pattern
            result = FSUtils.list_dir("test/dir")
            assert result == mock_items
            mock_iterdir.assert_called_once()
            mock_glob.assert_not_called()

            # Test listing with pattern
            mock_iterdir.reset_mock()
            result = FSUtils.list_dir("test/dir", pattern="*.txt")
            assert result == [Path("file1.txt")]
            mock_iterdir.assert_not_called()
            mock_glob.assert_called_once_with("*.txt")

            # Test directory does not exist
            mock_exists.return_value = False
            with pytest.raises(FileNotFoundError):
                FSUtils.list_dir("test/dir")

            # Test path is not a directory
            mock_exists.return_value = True
            mock_is_dir.return_value = False
            with pytest.raises(NotADirectoryError):
                FSUtils.list_dir("test/dir")

    def test_remove_file(self):
        """Test removing a file."""
        with patch("pathlib.Path.unlink") as mock_unlink:
            # Test removing file
            FSUtils.remove_file("test/file.txt")
            mock_unlink.assert_called_once()

            # Test with Path object
            mock_unlink.reset_mock()
            path_obj = Path("test/file.txt")
            FSUtils.remove_file(path_obj)
            mock_unlink.assert_called_once()

    def test_remove_dir(self):
        """Test removing a directory."""
        with patch("shutil.rmtree") as mock_rmtree:
            # Test removing directory
            FSUtils.remove_dir("test/dir")
            mock_rmtree.assert_called_once()

            # Test with Path object
            mock_rmtree.reset_mock()
            path_obj = Path("test/dir")
            FSUtils.remove_dir(path_obj)
            mock_rmtree.assert_called_once()
