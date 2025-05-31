"""Unit tests for ErrorHandler class."""

import traceback
from unittest.mock import patch, MagicMock

from create_sparc_py.utils import ErrorHandler


class TestErrorHandler:
    """Tests for the ErrorHandler class."""

    def test_categorize_file_not_found(self):
        """Test categorizing FileNotFoundError."""
        error = FileNotFoundError("File does not exist")
        category = ErrorHandler.categorize(error)

        assert category["type"] == "FILE_NOT_FOUND"
        assert category["recoverable"] is False
        assert category["message"] == "File or directory not found"

    def test_categorize_permission_error(self):
        """Test categorizing PermissionError."""
        error = PermissionError("Permission denied")
        category = ErrorHandler.categorize(error)

        assert category["type"] == "PERMISSION_DENIED"
        assert category["recoverable"] is False
        assert category["message"] == "Permission denied"

    def test_categorize_file_exists_error(self):
        """Test categorizing FileExistsError."""
        error = FileExistsError("File already exists")
        category = ErrorHandler.categorize(error)

        assert category["type"] == "FILE_EXISTS"
        assert category["recoverable"] is True
        assert category["message"] == "File or directory already exists"

    def test_categorize_unknown_error(self):
        """Test categorizing unknown error types."""
        error = ValueError("Invalid value")
        category = ErrorHandler.categorize(error)

        assert category["type"] == "UNKNOWN_ERROR"
        assert category["recoverable"] is False
        assert category["message"] == "Invalid value"

    def test_format_basic(self):
        """Test basic error formatting without verbose details."""
        error = FileNotFoundError("test.txt")
        formatted = ErrorHandler.format(error)

        assert "File or directory not found: test.txt" in formatted
        # No traceback should be included
        assert "\n" not in formatted

    @patch("traceback.format_exception")
    def test_format_verbose(self, mock_format_exception):
        """Test verbose error formatting with traceback."""
        # Create a mock error with a traceback
        error = MagicMock(spec=Exception)
        error.__str__.return_value = "Mock error"
        error.__traceback__ = "mock_traceback"

        # Mock the traceback.format_exception function
        mock_format_exception.return_value = [
            "Traceback Line 1\n",
            "Traceback Line 2\n",
        ]

        # Format the error with verbose=True
        formatted = ErrorHandler.format(error, verbose=True)

        # Verify correct behavior
        mock_format_exception.assert_called_once()
        assert "Mock error" in formatted
        assert "Traceback Line 1\nTraceback Line 2\n" in formatted
