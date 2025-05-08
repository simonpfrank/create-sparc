import unittest
import os
from pathlib import Path

from create_sparc_py.utils import path_utils, PathUtils


class TestPathUtils(unittest.TestCase):
    """Test suite for the PathUtils class."""

    def test_resolve(self):
        """Test resolving a path to absolute form."""
        # Test with a relative path
        result = PathUtils.resolve("test_dir")
        expected = Path("test_dir").resolve()
        self.assertEqual(expected, result)

        # Test with multiple path components
        result = PathUtils.resolve("test_dir", "subdir", "file.txt")
        expected = Path("test_dir/subdir/file.txt").resolve()
        self.assertEqual(expected, result)

    def test_join(self):
        """Test joining path components."""
        # Test with a single path
        result = PathUtils.join("test_dir")
        self.assertEqual(Path("test_dir"), result)

        # Test with multiple path components
        result = PathUtils.join("test_dir", "subdir", "file.txt")
        self.assertEqual(Path("test_dir/subdir/file.txt"), result)

    def test_is_absolute(self):
        """Test checking if a path is absolute."""
        # Test with a relative path
        self.assertFalse(PathUtils.is_absolute("test_dir"))

        # Test with an absolute path
        absolute_path = os.path.abspath("test_dir")
        self.assertTrue(PathUtils.is_absolute(absolute_path))

    def test_get_relative_path(self):
        """Test getting a relative path."""
        # Create path objects for testing
        base = Path("/base/path")
        path = Path("/base/path/subdir/file.txt")

        # Test getting relative path
        result = PathUtils.get_relative_path(path, base)
        self.assertEqual(Path("subdir/file.txt"), result)

    def test_get_name(self):
        """Test getting the name component of a path."""
        # Test with a file path
        self.assertEqual("file.txt", PathUtils.get_name("path/to/file.txt"))

        # Test with a directory path
        self.assertEqual("dir", PathUtils.get_name("path/to/dir"))

    def test_get_stem(self):
        """Test getting the stem component of a path."""
        # Test with a file path
        self.assertEqual("file", PathUtils.get_stem("path/to/file.txt"))

        # Test with a directory path
        self.assertEqual("dir", PathUtils.get_stem("path/to/dir"))

    def test_get_suffix(self):
        """Test getting the suffix component of a path."""
        # Test with a file path with extension
        self.assertEqual(".txt", PathUtils.get_suffix("path/to/file.txt"))

        # Test with a file path without extension
        self.assertEqual("", PathUtils.get_suffix("path/to/file"))

        # Test with a directory path
        self.assertEqual("", PathUtils.get_suffix("path/to/dir"))

    def test_get_parent(self):
        """Test getting the parent directory of a path."""
        # Test with a file path
        self.assertEqual(Path("path/to"), PathUtils.get_parent("path/to/file.txt"))

        # Test with a directory path
        self.assertEqual(Path("path"), PathUtils.get_parent("path/to"))

    def test_change_extension(self):
        """Test changing the extension of a path."""
        # Test with extension including dot
        self.assertEqual(
            Path("path/to/file.md"),
            PathUtils.change_extension("path/to/file.txt", ".md"),
        )

        # Test with extension without dot
        self.assertEqual(
            Path("path/to/file.md"),
            PathUtils.change_extension("path/to/file.txt", "md"),
        )

        # Test with empty extension (removes extension)
        self.assertEqual(
            Path("path/to/file"), PathUtils.change_extension("path/to/file.txt", "")
        )

    def test_singleton_instance(self):
        """Test that the singleton path_utils instance is exported."""
        self.assertIsInstance(path_utils, PathUtils)
