"""Tests for video converter implementation."""

from pathlib import Path
from unittest.mock import MagicMock, patch

from src.domain.entities import ConversionConfig, VideoFile, VideoFormat
from src.infrastructure.video_converter import MoviePyVideoConverter


@patch("src.infrastructure.video_converter.subprocess.run")
@patch("src.infrastructure.video_converter.ffmpeg.get_ffmpeg_exe")
def test_convert_success(mock_get_ffmpeg, mock_run, temp_dir):
    """Test successful conversion."""
    mock_get_ffmpeg.return_value = "ffmpeg"

    # Mock subprocess success
    mock_run.return_value = MagicMock(returncode=0)

    converter = MoviePyVideoConverter()

    avi_path = temp_dir / "test.avi"
    avi_path.write_text("fake")
    video = VideoFile(path=avi_path, format=VideoFormat.AVI)

    config = ConversionConfig(codec="copy", audio_codec="copy", skip_if_exists=False)

    # Mock output file creation so size can be read
    output_path = video.get_output_path()
    output_path.write_text("fake out")

    result = converter.convert(video, config)

    assert result.success is True
    assert result.output_path == output_path


@patch("src.infrastructure.video_converter.subprocess.run")
@patch("src.infrastructure.video_converter.ffmpeg.get_ffmpeg_exe")
def test_convert_failure(mock_get_ffmpeg, mock_run, temp_dir):
    """Test failed conversion."""
    mock_get_ffmpeg.return_value = "ffmpeg"
    mock_run.return_value = MagicMock(returncode=1, stderr="error")

    converter = MoviePyVideoConverter()

    avi_path = temp_dir / "test.avi"
    avi_path.write_text("fake")
    video = VideoFile(path=avi_path, format=VideoFormat.AVI)

    config = ConversionConfig(codec="libx264", audio_codec="aac", skip_if_exists=False, threads=2)

    result = converter.convert(video, config)

    assert result.success is False
    assert "FFmpeg error" in result.error_message


def test_convert_skip_existing(temp_dir):
    """Test skipping when output exists."""
    converter = MoviePyVideoConverter()

    avi_path = temp_dir / "test.avi"
    avi_path.write_text("fake")
    video = VideoFile(path=avi_path, format=VideoFormat.AVI)

    # Create existing output
    output_path = video.get_output_path()
    output_path.write_text("exists")

    config = ConversionConfig(skip_if_exists=True)
    result = converter.convert(video, config)

    assert result.success is True
    assert "skipped" in result.error_message


@patch("src.infrastructure.video_converter.subprocess.run")
@patch("src.infrastructure.video_converter.ffmpeg.get_ffmpeg_exe")
def test_is_valid_video(mock_get_ffmpeg, mock_run, temp_dir):
    """Test validation."""
    mock_get_ffmpeg.return_value = "ffmpeg"
    mock_run.return_value = MagicMock(returncode=0)

    converter = MoviePyVideoConverter()

    assert converter.is_valid_video(Path("nonexistent.avi")) is False

    avi_path = temp_dir / "test.avi"
    avi_path.write_text("fake")

    assert converter.is_valid_video(avi_path) is True
