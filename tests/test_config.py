"""Tests for configuration module."""

from pathlib import Path

import pytest
from pydantic import ValidationError

from src.config import Settings


def test_settings_defaults():
    """Test default settings values."""
    settings = Settings()

    assert settings.video_codec == "copy"
    assert settings.audio_codec == "copy"  # Changed to 'copy' for extreme speed
    assert settings.preset == "ultrafast"  # Changed to 'ultrafast' for extreme speed
    assert settings.crf == 30  # Changed to 30 for extreme speed
    assert settings.remove_source is True
    assert settings.skip_if_exists is True
    assert settings.max_retries == 3
    assert settings.max_workers == 4


def test_settings_parse_directories():
    """Test parsing comma-separated directories."""
    settings = Settings(conversion_directories="dir1,dir2,dir3")

    dirs = settings.get_conversion_directories()
    assert len(dirs) == 3
    assert Path("dir1") in dirs
    assert Path("dir2") in dirs


def test_settings_get_conversion_directories():
    """Test getting directories as Path objects."""
    settings = Settings(conversion_directories="dir1,dir2")

    paths = settings.get_conversion_directories()

    assert len(paths) == 2
    assert all(isinstance(p, Path) for p in paths)


def test_settings_validation():
    """Test settings validation."""
    # Valid CRF
    settings = Settings(crf=23)
    assert settings.crf == 23

    # Invalid CRF should be caught by pydantic
    with pytest.raises(ValidationError):
        Settings(crf=52)
