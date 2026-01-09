"""Domain entities for video conversion."""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path


class VideoFormat(str, Enum):
    """Supported video formats."""

    AVI = "avi"
    MP4 = "mp4"


class ConversionStatus(str, Enum):
    """Status of video conversion."""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class VideoFile:
    """Represents a video file to be processed."""

    path: Path
    format: VideoFormat
    size_bytes: int = 0
    status: ConversionStatus = ConversionStatus.PENDING
    created_at: datetime = field(default_factory=datetime.now)

    @property
    def filename(self) -> str:
        """Get the filename without path."""
        return self.path.name

    @property
    def directory(self) -> Path:
        """Get the directory containing the file."""
        return self.path.parent

    @property
    def size_mb(self) -> float:
        """Get file size in megabytes."""
        return self.size_bytes / (1024 * 1024)

    def is_avi(self) -> bool:
        """Check if the file is AVI format."""
        return self.format == VideoFormat.AVI

    def get_output_path(self) -> Path:
        """Get the output path for converted file."""
        return self.path.with_suffix(f".{VideoFormat.MP4.value}")


@dataclass
class ConversionResult:
    """Result of a video conversion operation."""

    video_file: VideoFile
    success: bool
    output_path: Path | None = None
    error_message: str | None = None
    duration_seconds: float = 0.0
    original_size_mb: float = 0.0
    converted_size_mb: float = 0.0

    @property
    def compression_ratio(self) -> float:
        """Calculate compression ratio (original/converted)."""
        if self.converted_size_mb > 0:
            return self.original_size_mb / self.converted_size_mb
        return 0.0

    @property
    def size_reduction_percent(self) -> float:
        """Calculate size reduction percentage."""
        if self.original_size_mb > 0:
            reduction = self.original_size_mb - self.converted_size_mb
            return (reduction / self.original_size_mb) * 100
        return 0.0


@dataclass
class ConversionConfig:
    """Configuration for video conversion."""

    codec: str = "libx264"
    audio_codec: str = "aac"
    preset: str = "medium"
    crf: int = 23  # Constant Rate Factor (0-51, lower is better quality)
    audio_bitrate: str = "128k"
    threads: int = 0  # 0 = auto-detect
    remove_source: bool = True
    skip_if_exists: bool = True
    max_retries: int = 3
    retry_delay_seconds: float = 1.0

    def __post_init__(self) -> None:
        """Validate configuration values."""
        if not 0 <= self.crf <= 51:
            raise ValueError("CRF must be between 0 and 51")
        if self.max_retries < 0:
            raise ValueError("max_retries must be non-negative")
        if self.retry_delay_seconds < 0:
            raise ValueError("retry_delay_seconds must be non-negative")
