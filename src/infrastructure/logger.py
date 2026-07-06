"""Logger implementation using loguru."""

import sys
from pathlib import Path

from loguru import logger

from src.domain.interfaces import ILogger


class LoguruLogger(ILogger):
    """Logger implementation using loguru library."""

    def __init__(
        self,
        log_file: Path | None = None,
        log_level: str = "INFO",
        rotation: str = "10 MB",
        retention: str = "1 week",
    ):
        """
        Initialize the logger.

        Args:
            log_file: Path to log file (optional)
            log_level: Minimum log level
            rotation: When to rotate log files
            retention: How long to keep old log files
        """
        # Remove default handler
        logger.remove()

        # Add console handler with colors
        logger.add(
            sys.stderr,
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
            level=log_level,
            colorize=True,
        )

        # Add file handler if specified
        if log_file:
            log_dir = log_file.parent
            log_dir.mkdir(parents=True, exist_ok=True)

            # Make logs folder hidden on Windows
            if sys.platform == "win32":
                import ctypes

                try:
                    # Set hidden attribute on Windows
                    FILE_ATTRIBUTE_HIDDEN = 0x02
                    ctypes.windll.kernel32.SetFileAttributesW(str(log_dir), FILE_ATTRIBUTE_HIDDEN)
                except Exception:
                    pass  # Ignore errors if setting hidden attribute fails

            logger.add(
                str(log_file),
                format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
                level=log_level,
                rotation=rotation,
                retention=retention,
                compression="zip",
            )

        self._logger = logger

    def debug(self, message: str, **kwargs) -> None:
        """Log debug message."""
        self._logger.debug(message, **kwargs)

    def info(self, message: str, **kwargs) -> None:
        """Log info message."""
        self._logger.info(message, **kwargs)

    def warning(self, message: str, **kwargs) -> None:
        """Log warning message."""
        self._logger.warning(message, **kwargs)

    def error(self, message: str, **kwargs) -> None:
        """Log error message."""
        self._logger.error(message, **kwargs)

    def exception(self, message: str, **kwargs) -> None:
        """Log exception with traceback."""
        self._logger.exception(message, **kwargs)
