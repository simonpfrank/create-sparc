"""Unit tests for Logger class."""

import pytest
from unittest.mock import patch

from create_sparc_py.utils import Logger


class TestLogger:
    """Tests for the Logger class."""

    def test_init(self):
        """Test Logger initialization."""
        logger = Logger()
        assert logger.get_level() == "info"

    def test_set_level_valid(self):
        """Test setting a valid log level."""
        logger = Logger()

        valid_levels = ["debug", "verbose", "info", "warning", "error"]
        for level in valid_levels:
            logger.set_level(level)
            assert logger.get_level() == level

    def test_set_level_invalid(self):
        """Test setting an invalid log level raises ValueError."""
        logger = Logger()

        with pytest.raises(ValueError):
            logger.set_level("invalid_level")

    def test_should_log(self):
        """Test the _should_log method."""
        logger = Logger()

        # Default level is "info" which is 2
        assert logger._should_log("debug") is False  # debug is 0
        assert logger._should_log("verbose") is False  # verbose is 1
        assert logger._should_log("info") is True  # info is 2
        assert logger._should_log("warning") is True  # warning is 3
        assert logger._should_log("error") is True  # error is 4

        # Set level to "debug"
        logger.set_level("debug")
        assert logger._should_log("debug") is True
        assert logger._should_log("verbose") is True
        assert logger._should_log("info") is True
        assert logger._should_log("warning") is True
        assert logger._should_log("error") is True

        # Set level to "error"
        logger.set_level("error")
        assert logger._should_log("debug") is False
        assert logger._should_log("verbose") is False
        assert logger._should_log("info") is False
        assert logger._should_log("warning") is False
        assert logger._should_log("error") is True

    @patch("builtins.print")
    def test_debug(self, mock_print):
        """Test debug log method."""
        logger = Logger()

        # Debug should not log at default level
        logger.debug("Debug message")
        mock_print.assert_not_called()

        # Debug should log at debug level
        logger.set_level("debug")
        logger.debug("Debug message")
        mock_print.assert_called_once()

    @patch("builtins.print")
    def test_verbose(self, mock_print):
        """Test verbose log method."""
        logger = Logger()

        # Verbose should not log at default level
        logger.verbose("Verbose message")
        mock_print.assert_not_called()

        # Verbose should log at verbose level
        logger.set_level("verbose")
        logger.verbose("Verbose message")
        mock_print.assert_called_once()

        # Verbose should also log at debug level
        mock_print.reset_mock()
        logger.set_level("debug")
        logger.verbose("Verbose message")
        mock_print.assert_called_once()

    @patch("builtins.print")
    def test_info(self, mock_print):
        """Test info log method."""
        logger = Logger()

        # Info should log at default level
        logger.info("Info message")
        mock_print.assert_called_once()

        # Info should not log at error level
        mock_print.reset_mock()
        logger.set_level("error")
        logger.info("Info message")
        mock_print.assert_not_called()

    @patch("builtins.print")
    def test_success(self, mock_print):
        """Test success log method."""
        logger = Logger()

        # Success should log at default level
        logger.success("Success message")
        mock_print.assert_called_once()

        # Success should not log at error level
        mock_print.reset_mock()
        logger.set_level("error")
        logger.success("Success message")
        mock_print.assert_not_called()

    @patch("builtins.print")
    def test_warning(self, mock_print):
        """Test warning log method."""
        logger = Logger()

        # Warning should log at default level
        logger.warning("Warning message")
        mock_print.assert_called_once()

        # Warning should not log at error level
        mock_print.reset_mock()
        logger.set_level("error")
        logger.warning("Warning message")
        mock_print.assert_not_called()

    @patch("builtins.print")
    def test_error(self, mock_print):
        """Test error log method."""
        logger = Logger()

        # Error should log at default level
        logger.error("Error message")
        mock_print.assert_called_once()

        # Error should log at error level too
        mock_print.reset_mock()
        logger.set_level("error")
        logger.error("Error message")
        mock_print.assert_called_once()
