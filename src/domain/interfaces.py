"""Domain interfaces for dependency inversion."""

from pathlib import Path
from typing import Protocol

from src.domain.entities import ConversionConfig, ConversionResult, VideoFile


class IVideoConverter(Protocol):
    """Interface for video conversion operations."""

    def convert(self, video_file: VideoFile, config: ConversionConfig) -> ConversionResult:
        """
        Convert a video file to MP4 format.

        Args:
            video_file: The video file to convert
            config: Conversion configuration

        Returns:
            ConversionResult with success status and details
        """
        ...

    def is_valid_video(self, file_path: Path) -> bool:
        """
        Check if a file is a valid video.

        Args:
            file_path: Path to the video file

        Returns:
            True if valid video, False otherwise
        """
        ...


class IFileRepository(Protocol):
    """Interface for file system operations."""

    def exists(self, file_path: Path) -> bool:
        """Check if a file exists."""
        ...

    def get_file_size(self, file_path: Path) -> int:
        """Get file size in bytes."""
        ...

    def remove(self, file_path: Path) -> bool:
        """Remove a file."""
        ...

    def is_file_locked(self, file_path: Path) -> bool:
        """Check if a file is locked/in use."""
        ...

    def find_avi_files(self, directory: Path, recursive: bool = True) -> list[Path]:
        """
        Find all AVI files in a directory.

        Args:
            directory: Directory to search
            recursive: Whether to search subdirectories

        Returns:
            List of paths to AVI files
        """
        ...


class ILogger(Protocol):
    """Interface for logging operations."""

    def debug(self, message: str, **kwargs) -> None:
        """Log debug message."""
        ...

    def info(self, message: str, **kwargs) -> None:
        """Log info message."""
        ...

    def warning(self, message: str, **kwargs) -> None:
        """Log warning message."""
        ...

    def error(self, message: str, **kwargs) -> None:
        """Log error message."""
        ...

    def exception(self, message: str, **kwargs) -> None:
        """Log exception with traceback."""
        ...
