import unittest
import os
import tempfile
import shutil
from pathlib import Path

from create_sparc_py.utils import fs_utils, FSUtils


class TestFSUtils(unittest.TestCase):
    """Test suite for the FSUtils class."""

    def setUp(self):
        """Set up temporary directory for file operations."""
        self.temp_dir = tempfile.mkdtemp()
        self.test_file_path = os.path.join(self.temp_dir, "test_file.txt")
        self.test_dir_path = os.path.join(self.temp_dir, "test_dir")
        self.test_content = "Test content"

        # Create a test file
        with open(self.test_file_path, "w") as f:
            f.write(self.test_content)

        # Create a test directory
        os.makedirs(self.test_dir_path, exist_ok=True)

    def tearDown(self):
        """Clean up temporary directory."""
        shutil.rmtree(self.temp_dir)

    def test_exists(self):
        """Test checking if a path exists."""
        # Test with an existing file
        self.assertTrue(FSUtils.exists(self.test_file_path))

        # Test with an existing directory
        self.assertTrue(FSUtils.exists(self.test_dir_path))

        # Test with a non-existent path
        self.assertFalse(FSUtils.exists(os.path.join(self.temp_dir, "non_existent")))

    def test_is_directory(self):
        """Test checking if a path is a directory."""
        # Test with a directory
        self.assertTrue(FSUtils.is_directory(self.test_dir_path))

        # Test with a file
        self.assertFalse(FSUtils.is_directory(self.test_file_path))

        # Test with a non-existent path (should return False)
        self.assertFalse(
            FSUtils.is_directory(os.path.join(self.temp_dir, "non_existent"))
        )

    def test_is_file(self):
        """Test checking if a path is a file."""
        # Test with a file
        self.assertTrue(FSUtils.is_file(self.test_file_path))

        # Test with a directory
        self.assertFalse(FSUtils.is_file(self.test_dir_path))

        # Test with a non-existent path (should return False)
        self.assertFalse(FSUtils.is_file(os.path.join(self.temp_dir, "non_existent")))

    def test_read_file(self):
        """Test reading file contents."""
        # Test reading an existing file
        content = FSUtils.read_file(self.test_file_path)
        self.assertEqual(self.test_content, content)

        # Test reading a non-existent file (should raise FileNotFoundError)
        with self.assertRaises(FileNotFoundError):
            FSUtils.read_file(os.path.join(self.temp_dir, "non_existent"))

    def test_write_file(self):
        """Test writing content to a file."""
        # Test writing to a new file
        new_file_path = os.path.join(self.temp_dir, "new_file.txt")
        new_content = "New file content"
        FSUtils.write_file(new_file_path, new_content)

        # Verify the content was written correctly
        with open(new_file_path, "r") as f:
            self.assertEqual(new_content, f.read())

        # Test overwriting an existing file
        overwrite_content = "Overwrite content"
        FSUtils.write_file(self.test_file_path, overwrite_content)

        # Verify the content was overwritten
        with open(self.test_file_path, "r") as f:
            self.assertEqual(overwrite_content, f.read())

    def test_copy_file(self):
        """Test copying a file."""
        # Test copying to a new location
        dest_path = os.path.join(self.temp_dir, "copy_file.txt")
        FSUtils.copy_file(self.test_file_path, dest_path)

        # Verify the file was copied correctly
        self.assertTrue(os.path.exists(dest_path))
        with open(dest_path, "r") as f:
            self.assertEqual(self.test_content, f.read())

        # Test copying a non-existent file (should raise FileNotFoundError)
        with self.assertRaises(FileNotFoundError):
            FSUtils.copy_file(os.path.join(self.temp_dir, "non_existent"), dest_path)

    def test_copy_dir(self):
        """Test copying a directory."""
        # Create a file in the test directory
        test_subfile_path = os.path.join(self.test_dir_path, "subfile.txt")
        with open(test_subfile_path, "w") as f:
            f.write("Subfile content")

        # Test copying to a new location
        dest_dir_path = os.path.join(self.temp_dir, "copy_dir")
        FSUtils.copy_dir(self.test_dir_path, dest_dir_path)

        # Verify the directory was copied correctly
        self.assertTrue(os.path.exists(dest_dir_path))
        self.assertTrue(os.path.exists(os.path.join(dest_dir_path, "subfile.txt")))

        # Test copying a non-existent directory (should raise FileNotFoundError)
        with self.assertRaises(FileNotFoundError):
            FSUtils.copy_dir(os.path.join(self.temp_dir, "non_existent"), dest_dir_path)

    def test_create_dir(self):
        """Test creating a directory."""
        # Test creating a new directory
        new_dir_path = os.path.join(self.temp_dir, "new_dir")
        FSUtils.create_dir(new_dir_path)

        # Verify the directory was created
        self.assertTrue(os.path.exists(new_dir_path))
        self.assertTrue(os.path.isdir(new_dir_path))

        # Test creating nested directories
        nested_dir_path = os.path.join(self.temp_dir, "nested", "dirs")
        FSUtils.create_dir(nested_dir_path)

        # Verify the nested directories were created
        self.assertTrue(os.path.exists(nested_dir_path))
        self.assertTrue(os.path.isdir(nested_dir_path))

    def test_list_dir(self):
        """Test listing directory contents."""
        # Create some files in the test directory
        file1_path = os.path.join(self.test_dir_path, "file1.txt")
        file2_path = os.path.join(self.test_dir_path, "file2.py")
        with open(file1_path, "w") as f:
            f.write("File 1 content")
        with open(file2_path, "w") as f:
            f.write("File 2 content")

        # Test listing all directory contents
        contents = FSUtils.list_dir(self.test_dir_path)
        self.assertEqual(2, len(contents))
        self.assertTrue(
            Path(file1_path) in contents or Path(file1_path).resolve() in contents
        )
        self.assertTrue(
            Path(file2_path) in contents or Path(file2_path).resolve() in contents
        )

        # Test listing with a pattern
        txt_files = FSUtils.list_dir(self.test_dir_path, "*.txt")
        self.assertEqual(1, len(txt_files))
        self.assertTrue(
            Path(file1_path) in txt_files or Path(file1_path).resolve() in txt_files
        )

    def test_remove_file(self):
        """Test removing a file."""
        # Test removing an existing file
        FSUtils.remove_file(self.test_file_path)
        self.assertFalse(os.path.exists(self.test_file_path))

        # Test removing a non-existent file (should raise FileNotFoundError)
        with self.assertRaises(FileNotFoundError):
            FSUtils.remove_file(os.path.join(self.temp_dir, "non_existent"))

    def test_remove_dir(self):
        """Test removing a directory."""
        # Test removing an existing directory
        FSUtils.remove_dir(self.test_dir_path)
        self.assertFalse(os.path.exists(self.test_dir_path))

        # Test removing a non-existent directory (should raise FileNotFoundError)
        with self.assertRaises(FileNotFoundError):
            FSUtils.remove_dir(os.path.join(self.temp_dir, "non_existent"))

    def test_singleton_instance(self):
        """Test that the singleton fs_utils instance is exported."""
        self.assertIsInstance(fs_utils, FSUtils)
