"""Dependency injection container."""


from src.application.use_cases.convert_videos import ConvertVideosUseCase
from src.config import Settings
from src.domain.entities import ConversionConfig
from src.infrastructure.file_repository import FileSystemRepository
from src.infrastructure.logger import LoguruLogger
from src.infrastructure.video_converter import MoviePyVideoConverter


class Container:
    """Dependency injection container."""

    def __init__(self, settings: Settings):
        """
        Initialize the container with settings.

        Args:
            settings: Application settings
        """
        self.settings = settings
        self._logger = None
        self._file_repository = None
        self._video_converter = None
        self._convert_videos_use_case = None

    @property
    def logger(self):
        """Get logger instance (singleton)."""
        if self._logger is None:
            log_file = self.settings.get_log_file_path()
            self._logger = LoguruLogger(
                log_file=log_file,
                log_level=self.settings.log_level,
                rotation=self.settings.log_rotation,
                retention=self.settings.log_retention,
            )
        return self._logger

    @property
    def file_repository(self):
        """Get file repository instance (singleton)."""
        if self._file_repository is None:
            self._file_repository = FileSystemRepository()
        return self._file_repository

    @property
    def video_converter(self):
        """Get video converter instance (singleton)."""
        if self._video_converter is None:
            self._video_converter = MoviePyVideoConverter()
        return self._video_converter

    @property
    def convert_videos_use_case(self):
        """Get convert videos use case instance (singleton)."""
        if self._convert_videos_use_case is None:
            self._convert_videos_use_case = ConvertVideosUseCase(
                converter=self.video_converter,
                file_repository=self.file_repository,
                logger=self.logger,
                max_workers=self.settings.max_workers,
            )
        return self._convert_videos_use_case

    def get_conversion_config(self) -> ConversionConfig:
        """Get conversion configuration from settings."""
        return ConversionConfig(
            codec=self.settings.video_codec,
            audio_codec=self.settings.audio_codec,
            preset=self.settings.preset,
            crf=self.settings.crf,
            audio_bitrate=self.settings.audio_bitrate,
            threads=self.settings.threads,
            remove_source=self.settings.remove_source,
            skip_if_exists=self.settings.skip_if_exists,
            max_retries=self.settings.max_retries,
            retry_delay_seconds=self.settings.retry_delay_seconds,
        )
