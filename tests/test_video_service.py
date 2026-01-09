"""Tests for video conversion service."""


from src.application.services.video_service import VideoConversionService
from src.domain.entities import ConversionResult, ConversionStatus, VideoFormat


def test_create_video_file(mock_video_converter, mock_file_repository, mock_logger, temp_dir):
    """Test creating a VideoFile entity."""
    service = VideoConversionService(mock_video_converter, mock_file_repository, mock_logger)

    test_file = temp_dir / "test.avi"
    test_file.write_text("content")

    mock_file_repository.get_file_size.return_value = len("content")

    video = service.create_video_file(test_file)

    assert video.path == test_file
    assert video.format == VideoFormat.AVI
    assert video.size_bytes == len("content")


def test_convert_video_success(
    mock_video_converter, mock_file_repository, mock_logger, sample_video_file, conversion_config
):
    """Test successful video conversion."""
    service = VideoConversionService(mock_video_converter, mock_file_repository, mock_logger)

    # Mock successful conversion
    mock_result = ConversionResult(
        video_file=sample_video_file,
        success=True,
        output_path=sample_video_file.get_output_path(),
        original_size_mb=10.0,
        converted_size_mb=5.0,
        duration_seconds=1.5,
    )
    mock_video_converter.convert.return_value = mock_result
    mock_file_repository.is_file_locked.return_value = False

    result = service.convert_video(sample_video_file, conversion_config)

    assert result.success is True
    assert sample_video_file.status == ConversionStatus.COMPLETED
    mock_logger.info.assert_called()


def test_convert_video_file_locked(
    mock_video_converter, mock_file_repository, mock_logger, sample_video_file, conversion_config
):
    """Test conversion when file is locked."""
    service = VideoConversionService(mock_video_converter, mock_file_repository, mock_logger)

    mock_file_repository.is_file_locked.return_value = True

    result = service.convert_video(sample_video_file, conversion_config)

    assert result.success is False
    assert sample_video_file.status == ConversionStatus.SKIPPED
    assert "locked" in result.error_message.lower()


def test_convert_video_with_retry(
    mock_video_converter, mock_file_repository, mock_logger, sample_video_file, conversion_config
):
    """Test conversion with retry logic."""
    service = VideoConversionService(mock_video_converter, mock_file_repository, mock_logger)

    # First attempt fails, second succeeds
    failed_result = ConversionResult(
        video_file=sample_video_file, success=False, error_message="Temporary error"
    )
    success_result = ConversionResult(
        video_file=sample_video_file,
        success=True,
        output_path=sample_video_file.get_output_path(),
    )

    mock_video_converter.convert.side_effect = [failed_result, success_result]
    mock_file_repository.is_file_locked.return_value = False

    conversion_config.max_retries = 2
    conversion_config.retry_delay_seconds = 0.01  # Fast retry for testing

    result = service.convert_video(sample_video_file, conversion_config)

    assert result.success is True
    assert mock_video_converter.convert.call_count == 2
