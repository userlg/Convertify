"""Tests for domain entities."""

from pathlib import Path

import pytest

from src.domain.entities import (
    ConversionConfig,
    ConversionResult,
    ConversionStatus,
    VideoFile,
    VideoFormat,
)


def test_video_file_creation():
    """Test VideoFile entity creation."""
    path = Path("test.avi")
    video = VideoFile(path=path, format=VideoFormat.AVI, size_bytes=1024)

    assert video.path == path
    assert video.format == VideoFormat.AVI
    assert video.size_bytes == 1024
    assert video.status == ConversionStatus.PENDING


def test_video_file_properties():
    """Test VideoFile properties."""
    path = Path("dir/test.avi")
    video = VideoFile(path=path, format=VideoFormat.AVI, size_bytes=1024 * 1024)

    assert video.filename == "test.avi"
    assert video.directory == Path("dir")
    assert video.size_mb == 1.0
    assert video.is_avi() is True


def test_video_file_output_path():
    """Test VideoFile output path generation."""
    video = VideoFile(path=Path("test.avi"), format=VideoFormat.AVI)
    assert video.get_output_path() == Path("test.mp4")


def test_conversion_result_properties():
    """Test ConversionResult properties."""
    video = VideoFile(path=Path("test.avi"), format=VideoFormat.AVI)
    result = ConversionResult(
        video_file=video,
        success=True,
        original_size_mb=10.0,
        converted_size_mb=5.0,
    )

    assert result.compression_ratio == 2.0
    assert result.size_reduction_percent == 50.0


def test_conversion_config_validation():
    """Test ConversionConfig validation."""
    # Valid config
    config = ConversionConfig(crf=23)
    assert config.crf == 23

    # Invalid CRF
    with pytest.raises(ValueError, match="CRF must be between 0 and 51"):
        ConversionConfig(crf=52)

    # Invalid max_retries
    with pytest.raises(ValueError, match="max_retries must be non-negative"):
        ConversionConfig(max_retries=-1)


def test_conversion_config_defaults():
    """Test ConversionConfig default values."""
    config = ConversionConfig()

    assert config.codec == "libx264"
    assert config.audio_codec == "aac"
    assert config.preset == "medium"
    assert config.crf == 23
    assert config.remove_source is True
    assert config.skip_if_exists is True
    assert config.max_retries == 3
