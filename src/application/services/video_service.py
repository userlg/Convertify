"""Video conversion service."""

import time
from pathlib import Path

from src.domain.entities import (
    ConversionConfig,
    ConversionResult,
    ConversionStatus,
    VideoFile,
    VideoFormat,
)
from src.domain.interfaces import IFileRepository, ILogger, IVideoConverter


class VideoConversionService:
    """Service for handling video conversion operations."""

    def __init__(
        self,
        converter: IVideoConverter,
        file_repository: IFileRepository,
        logger: ILogger,
    ):
        """
        Initialize the video conversion service.

        Args:
            converter: Video converter implementation
            file_repository: File repository implementation
            logger: Logger implementation
        """
        self.converter = converter
        self.file_repository = file_repository
        self.logger = logger

    def convert_video(self, video_file: VideoFile, config: ConversionConfig) -> ConversionResult:
        """
        Convert a single video file with retry logic.

        Args:
            video_file: The video file to convert
            config: Conversion configuration

        Returns:
            ConversionResult with success status and details
        """
        self.logger.info(f"Starting conversion: {video_file.filename}")

        # Check if file is locked
        if self.file_repository.is_file_locked(video_file.path):
            self.logger.warning(f"File is locked, skipping: {video_file.filename}")
            video_file.status = ConversionStatus.SKIPPED
            return ConversionResult(
                video_file=video_file,
                success=False,
                error_message="File is locked or in use",
            )

        # Retry logic
        last_error = None
        for attempt in range(config.max_retries):
            try:
                video_file.status = ConversionStatus.IN_PROGRESS
                result = self.converter.convert(video_file, config)

                if result.success:
                    video_file.status = ConversionStatus.COMPLETED
                    self.logger.info(
                        f"Conversion successful: {video_file.filename} "
                        f"({result.original_size_mb:.2f}MB -> {result.converted_size_mb:.2f}MB, "
                        f"{result.duration_seconds:.2f}s)"
                    )

                    # Remove source file if configured
                    if config.remove_source and result.output_path:
                        if self.file_repository.remove(video_file.path):
                            self.logger.debug(f"Removed source file: {video_file.filename}")
                        else:
                            self.logger.warning(
                                f"Failed to remove source file: {video_file.filename}"
                            )

                    return result
                else:
                    last_error = result.error_message
                    if attempt < config.max_retries - 1:
                        self.logger.warning(
                            f"Conversion failed (attempt {attempt + 1}/{config.max_retries}): "
                            f"{video_file.filename} - {result.error_message}"
                        )
                        time.sleep(config.retry_delay_seconds)
                    else:
                        video_file.status = ConversionStatus.FAILED
                        self.logger.error(
                            f"Conversion failed after {config.max_retries} attempts: "
                            f"{video_file.filename}"
                        )
                        return result

            except Exception as e:
                last_error = str(e)
                if attempt < config.max_retries - 1:
                    self.logger.warning(
                        f"Exception during conversion (attempt {attempt + 1}/{config.max_retries}): "
                        f"{video_file.filename} - {str(e)}"
                    )
                    time.sleep(config.retry_delay_seconds)
                else:
                    video_file.status = ConversionStatus.FAILED
                    self.logger.exception(
                        f"Exception after {config.max_retries} attempts: {video_file.filename}"
                    )

        # All retries failed
        video_file.status = ConversionStatus.FAILED
        return ConversionResult(
            video_file=video_file,
            success=False,
            error_message=last_error or "Unknown error",
        )

    def create_video_file(self, file_path: Path) -> VideoFile:
        """
        Create a VideoFile entity from a file path.

        Args:
            file_path: Path to the video file

        Returns:
            VideoFile entity
        """
        size = self.file_repository.get_file_size(file_path)
        return VideoFile(
            path=file_path,
            format=VideoFormat.AVI,
            size_bytes=size,
        )
