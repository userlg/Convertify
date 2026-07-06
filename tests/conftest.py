"""Shared test fixtures and configuration."""

import tempfile
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from src.domain.entities import ConversionConfig, VideoFile, VideoFormat
from src.infrastructure.file_repository import FileSystemRepository
from src.infrastructure.video_converter import MoviePyVideoConverter


@pytest.fixture
def temp_dir():
    """Create a temporary directory for tests."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def sample_avi_file(temp_dir):
    """Create a sample AVI file for testing."""
    avi_path = temp_dir / "test_video.avi"
    avi_path.write_text("fake avi content")
    return avi_path


@pytest.fixture
def sample_video_file(sample_avi_file):
    """Create a VideoFile entity for testing."""
    return VideoFile(
        path=sample_avi_file,
        format=VideoFormat.AVI,
        size_bytes=len("fake avi content"),
    )


@pytest.fixture
def conversion_config():
    """Create a default conversion config for testing."""
    return ConversionConfig(
        codec="libx264",
        audio_codec="aac",
        preset="medium",
        crf=23,
        remove_source=False,  # Don't remove in tests
        skip_if_exists=True,
        max_retries=1,  # Reduce retries in tests
    )


@pytest.fixture
def mock_logger():
    """Create a mock logger for testing."""
    logger = MagicMock()
    logger.debug = MagicMock()
    logger.info = MagicMock()
    logger.warning = MagicMock()
    logger.error = MagicMock()
    logger.exception = MagicMock()
    return logger


@pytest.fixture
def mock_file_repository():
    """Create a mock file repository for testing."""
    repo = MagicMock(spec=FileSystemRepository)
    repo.exists = MagicMock(return_value=True)
    repo.get_file_size = MagicMock(return_value=1024)
    repo.remove = MagicMock(return_value=True)
    repo.is_file_locked = MagicMock(return_value=False)
    repo.find_avi_files = MagicMock(return_value=[])
    return repo


@pytest.fixture
def mock_video_converter():
    """Create a mock video converter for testing."""
    converter = MagicMock(spec=MoviePyVideoConverter)
    converter.is_valid_video = MagicMock(return_value=True)
    return converter
