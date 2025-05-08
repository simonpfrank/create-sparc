import unittest
from create_sparc_py.utils import error_handler, ErrorHandler


class TestErrorHandler(unittest.TestCase):
    """Test suite for the ErrorHandler class."""

    def test_categorize_file_not_found(self):
        """Test that FileNotFoundError is categorized correctly."""
        error = FileNotFoundError("Test file not found error")
        result = ErrorHandler.categorize(error)

        self.assertEqual("FILE_NOT_FOUND", result["type"])
        self.assertEqual(False, result["recoverable"])
        self.assertEqual("File or directory not found", result["message"])

    def test_categorize_permission_error(self):
        """Test that PermissionError is categorized correctly."""
        error = PermissionError("Test permission error")
        result = ErrorHandler.categorize(error)

        self.assertEqual("PERMISSION_DENIED", result["type"])
        self.assertEqual(False, result["recoverable"])
        self.assertEqual("Permission denied", result["message"])

    def test_categorize_file_exists_error(self):
        """Test that FileExistsError is categorized correctly."""
        error = FileExistsError("Test file exists error")
        result = ErrorHandler.categorize(error)

        self.assertEqual("FILE_EXISTS", result["type"])
        self.assertEqual(True, result["recoverable"])
        self.assertEqual("File or directory already exists", result["message"])

    def test_categorize_unknown_error(self):
        """Test that unknown errors are categorized correctly."""
        error = ValueError("Test value error")
        result = ErrorHandler.categorize(error)

        self.assertEqual("UNKNOWN_ERROR", result["type"])
        self.assertEqual(False, result["recoverable"])
        self.assertEqual("Test value error", result["message"])

    def test_format_simple_error(self):
        """Test formatting a simple error message."""
        error = ValueError("Test value error")
        formatted = ErrorHandler.format(error)

        self.assertIn("UNKNOWN_ERROR", formatted)
        self.assertIn("Test value error", formatted)

    def test_format_verbose_error(self):
        """Test formatting a verbose error message."""
        error = ValueError("Test value error")
        formatted = ErrorHandler.format(error, verbose=True)

        self.assertIn("UNKNOWN_ERROR", formatted)
        self.assertIn("Test value error", formatted)
        # When verbose is True, should include traceback info
        self.assertIn("Traceback", formatted, "Verbose format should include traceback")

    def test_singleton_instance(self):
        """Test that the singleton error_handler instance is exported."""
        self.assertIsInstance(error_handler, ErrorHandler)
