"""Unit tests for PathUtils class."""

from pathlib import Path
from unittest.mock import patch

import pytest

from create_sparc_py.utils import PathUtils


class TestPathUtils:
    """Tests for the PathUtils class."""

    def test_resolve(self):
        """Test resolving a path to its absolute form."""
        with patch("pathlib.Path.resolve") as mock_resolve:
            mock_resolve.return_value = Path("/absolute/path")

            # Test with string path
            result = PathUtils.resolve("test/path")
            assert isinstance(result, Path)
            mock_resolve.assert_called_once()

            # Test with Path object
            mock_resolve.reset_mock()
            path_obj = Path("test/path")
            PathUtils.resolve(path_obj)
            mock_resolve.assert_called_once()

            # Test with multiple path components
            mock_resolve.reset_mock()
            PathUtils.resolve("test", "path", "file.txt")
            mock_resolve.assert_called_once()

    def test_join(self):
        """Test joining path components."""
        # Test with string path
        result = PathUtils.join("test", "path")
        assert result == Path("test/path")

        # Test with Path object
        path_obj = Path("test")
        result = PathUtils.join(path_obj, "path")
        assert result == Path("test/path")

        # Test with multiple path components
        result = PathUtils.join("test", "path", "file.txt")
        assert result == Path("test/path/file.txt")

    def test_is_absolute(self):
        """Test checking if a path is absolute."""
        # Test with absolute path
        with patch("pathlib.Path.is_absolute") as mock_is_absolute:
            mock_is_absolute.return_value = True
            assert PathUtils.is_absolute("/absolute/path") is True
            mock_is_absolute.assert_called_once()

            # Test with relative path
            mock_is_absolute.reset_mock()
            mock_is_absolute.return_value = False
            assert PathUtils.is_absolute("relative/path") is False
            mock_is_absolute.assert_called_once()

            # Test with Path object
            mock_is_absolute.reset_mock()
            path_obj = Path("test/path")
            PathUtils.is_absolute(path_obj)
            mock_is_absolute.assert_called_once()

    def test_get_relative_path(self):
        """Test getting a path relative to a base directory."""
        with patch("pathlib.Path.relative_to") as mock_relative_to:
            mock_relative_to.return_value = Path("file.txt")

            # Test with string paths
            result = PathUtils.get_relative_path("/base/path/file.txt", "/base")
            assert isinstance(result, Path)
            mock_relative_to.assert_called_once()

            # Test with Path objects
            mock_relative_to.reset_mock()
            path_obj = Path("/base/path/file.txt")
            base_obj = Path("/base")
            PathUtils.get_relative_path(path_obj, base_obj)
            mock_relative_to.assert_called_once()

    def test_get_name(self):
        """Test getting the name component of a path."""
        # Test with file path
        assert PathUtils.get_name("test/path/file.txt") == "file.txt"

        # Test with directory path
        assert PathUtils.get_name("test/path/dir") == "dir"

        # Test with Path object
        path_obj = Path("test/path/file.txt")
        assert PathUtils.get_name(path_obj) == "file.txt"

    def test_get_stem(self):
        """Test getting the stem component of a path."""
        # Test with file path
        assert PathUtils.get_stem("test/path/file.txt") == "file"

        # Test with no extension
        assert PathUtils.get_stem("test/path/file") == "file"

        # Test with multiple extensions
        assert PathUtils.get_stem("test/path/file.tar.gz") == "file.tar"

        # Test with Path object
        path_obj = Path("test/path/file.txt")
        assert PathUtils.get_stem(path_obj) == "file"

    def test_get_suffix(self):
        """Test getting the suffix component of a path."""
        # Test with file path
        assert PathUtils.get_suffix("test/path/file.txt") == ".txt"

        # Test with no extension
        assert PathUtils.get_suffix("test/path/file") == ""

        # Test with multiple extensions
        assert PathUtils.get_suffix("test/path/file.tar.gz") == ".gz"

        # Test with Path object
        path_obj = Path("test/path/file.txt")
        assert PathUtils.get_suffix(path_obj) == ".txt"

    def test_get_parent(self):
        """Test getting the parent directory of a path."""
        # Test with file path
        assert PathUtils.get_parent("test/path/file.txt") == Path("test/path")

        # Test with directory path
        assert PathUtils.get_parent("test/path") == Path("test")

        # Test with root path
        assert PathUtils.get_parent("/") == Path("/")

        # Test with Path object
        path_obj = Path("test/path/file.txt")
        assert PathUtils.get_parent(path_obj) == Path("test/path")

    def test_change_extension(self):
        """Test changing the extension of a path."""
        # Test changing extension with dot
        assert PathUtils.change_extension("test/path/file.txt", ".md") == Path(
            "test/path/file.md"
        )

        # Test changing extension without dot
        assert PathUtils.change_extension("test/path/file.txt", "md") == Path(
            "test/path/file.md"
        )

        # Test with empty extension
        assert PathUtils.change_extension("test/path/file.txt", "") == Path(
            "test/path/file"
        )

        # Test with Path object
        path_obj = Path("test/path/file.txt")
        assert PathUtils.change_extension(path_obj, ".md") == Path("test/path/file.md")
