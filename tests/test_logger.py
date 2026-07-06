"""Tests for infrastructure logger."""

from loguru import logger as loguru_logger

from src.infrastructure.logger import LoguruLogger


def test_logger_initialization(temp_dir):
    """Test logger initializes correctly."""
    log_file = temp_dir / "test.log"
    log_instance = LoguruLogger(log_file=log_file, log_level="DEBUG")

    assert log_instance._logger is not None

    # Test methods don't crash
    log_instance.debug("test debug")
    log_instance.info("test info")
    log_instance.warning("test warning")
    log_instance.error("test error")

    try:
        raise ValueError("test exception")
    except ValueError:
        log_instance.exception("test exception log")

    # Clean up loguru handlers so the log file is released
    # before the temp directory is deleted (Windows locks open files)
    loguru_logger.remove()


def test_logger_initialization_no_file():
    """Test logger initializes correctly without a file."""
    log_instance = LoguruLogger(log_file=None, log_level="DEBUG")
    assert log_instance._logger is not None
    log_instance.info("should not crash")
