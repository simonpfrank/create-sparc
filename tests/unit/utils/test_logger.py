import unittest
from unittest.mock import patch
from io import StringIO
import sys

from create_sparc_py.utils import logger, Logger


class TestLogger(unittest.TestCase):
    """Test suite for the Logger class."""

    def setUp(self):
        """Set up tests by creating a fresh Logger instance."""
        self.logger = Logger()
        # Reset the logger level before each test
        self.logger.set_level("info")

    @patch("sys.stdout", new_callable=StringIO)
    def test_info_message(self, mock_stdout):
        """Test that info messages are printed correctly."""
        self.logger.info("Test info message")
        self.assertIn("Test info message", mock_stdout.getvalue())

    @patch("sys.stdout", new_callable=StringIO)
    def test_success_message(self, mock_stdout):
        """Test that success messages are printed correctly."""
        self.logger.success("Test success message")
        self.assertIn("✓ Test success message", mock_stdout.getvalue())

    @patch("sys.stdout", new_callable=StringIO)
    def test_warning_message(self, mock_stdout):
        """Test that warning messages are printed correctly."""
        self.logger.warning("Test warning message")
        self.assertIn("⚠ Test warning message", mock_stdout.getvalue())

    @patch("sys.stdout", new_callable=StringIO)
    def test_error_message(self, mock_stdout):
        """Test that error messages are printed correctly."""
        self.logger.error("Test error message")
        self.assertIn("✖ Test error message", mock_stdout.getvalue())

    @patch("sys.stdout", new_callable=StringIO)
    def test_debug_message_not_shown_at_info_level(self, mock_stdout):
        """Test that debug messages are not shown at info level."""
        self.logger.set_level("info")
        self.logger.debug("Test debug message")
        self.assertEqual("", mock_stdout.getvalue())

    @patch("sys.stdout", new_callable=StringIO)
    def test_debug_message_shown_at_debug_level(self, mock_stdout):
        """Test that debug messages are shown at debug level."""
        self.logger.set_level("debug")
        self.logger.debug("Test debug message")
        self.assertIn("[debug] Test debug message", mock_stdout.getvalue())

    @patch("sys.stdout", new_callable=StringIO)
    def test_verbose_message_not_shown_at_info_level(self, mock_stdout):
        """Test that verbose messages are not shown at info level."""
        self.logger.set_level("info")
        self.logger.verbose("Test verbose message")
        self.assertEqual("", mock_stdout.getvalue())

    @patch("sys.stdout", new_callable=StringIO)
    def test_verbose_message_shown_at_verbose_level(self, mock_stdout):
        """Test that verbose messages are shown at verbose level."""
        self.logger.set_level("verbose")
        self.logger.verbose("Test verbose message")
        self.assertIn("[verbose] Test verbose message", mock_stdout.getvalue())

    def test_set_invalid_level_raises_error(self):
        """Test that setting an invalid level raises a ValueError."""
        with self.assertRaises(ValueError):
            self.logger.set_level("invalid_level")

    def test_get_level(self):
        """Test that get_level returns the current logging level."""
        self.logger.set_level("debug")
        self.assertEqual("debug", self.logger.get_level())

    def test_singleton_instance(self):
        """Test that the singleton logger instance is exported."""
        self.assertIsInstance(logger, Logger)
