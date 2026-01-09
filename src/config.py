"""Configuration management using pydantic-settings."""

from pathlib import Path

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Conversion directories
    conversion_directories: list[str] = Field(
        default_factory=list,
        description="Comma-separated list of directories to scan for AVI files",
    )

    # Conversion settings
    video_codec: str = Field(default="libx264", description="Video codec for conversion")
    audio_codec: str = Field(default="aac", description="Audio codec for conversion")
    preset: str = Field(
        default="medium",
        description="Encoding preset (ultrafast, superfast, veryfast, faster, fast, medium, slow, slower, veryslow)",
    )
    crf: int = Field(
        default=23, ge=0, le=51, description="Constant Rate Factor (0-51, lower is better quality)"
    )
    audio_bitrate: str = Field(default="128k", description="Audio bitrate")
    threads: int = Field(default=0, ge=0, description="Number of threads (0 = auto)")

    # Behavior settings
    remove_source: bool = Field(
        default=True, description="Remove source AVI file after successful conversion"
    )
    skip_if_exists: bool = Field(
        default=True, description="Skip conversion if output MP4 already exists"
    )
    max_retries: int = Field(
        default=3, ge=0, description="Maximum retry attempts for failed conversions"
    )
    retry_delay_seconds: float = Field(
        default=1.0, ge=0, description="Delay between retry attempts in seconds"
    )

    # Performance settings
    max_workers: int = Field(default=4, ge=1, description="Maximum number of parallel workers")

    # Logging settings
    log_level: str = Field(default="INFO", description="Logging level")
    log_file: str | None = Field(default="logs/convertify.log", description="Log file path")
    log_rotation: str = Field(default="10 MB", description="Log rotation size")
    log_retention: str = Field(default="1 week", description="Log retention period")

    @field_validator("conversion_directories", mode="before")
    @classmethod
    def parse_directories(cls, v):
        """Parse comma-separated directories."""
        if isinstance(v, str):
            if not v.strip():
                return []
            return [d.strip() for d in v.split(",") if d.strip()]
        if isinstance(v, list):
            return v
        return []

    def get_conversion_directories(self) -> list[Path]:
        """Get conversion directories as Path objects."""
        return [Path(d) for d in self.conversion_directories if d]

    def get_log_file_path(self) -> Path | None:
        """Get log file path as Path object."""
        if self.log_file:
            return Path(self.log_file)
        return None


def load_settings() -> Settings:
    """Load settings from environment variables and .env file."""
    return Settings()
