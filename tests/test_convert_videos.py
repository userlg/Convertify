"""Tests for convert videos use case."""

from pathlib import Path
from unittest.mock import MagicMock

from src.application.use_cases.convert_videos import ConvertVideosUseCase
from src.domain.entities import ConversionResult


def test_convert_videos_execute(
    mock_video_converter, mock_file_repository, mock_logger, conversion_config, sample_video_file
):
    """Test batch conversion execution."""
    # Setup mocks
    # File discovery should find 1 file
    use_case = ConvertVideosUseCase(mock_video_converter, mock_file_repository, mock_logger)

    # Mock the internal file service to return a list of paths
    use_case.file_service = MagicMock()
    use_case.file_service.find_videos_in_directories.return_value = [sample_video_file.path]

    # Mock video service to return a success result
    use_case.video_service = MagicMock()
    use_case.video_service.create_video_file.return_value = sample_video_file

    success_result = ConversionResult(
        video_file=sample_video_file, success=True, output_path=Path("out.mp4")
    )
    use_case.video_service.convert_video.return_value = success_result

    # Execute
    progress_calls = []

    def progress_callback(current, total):
        progress_calls.append((current, total))

    results = use_case.execute([Path("test_dir")], conversion_config, progress_callback)

    # Verify
    assert len(results) == 1
    assert results[0].success is True
    assert len(progress_calls) == 1
    assert progress_calls[0] == (1, 1)


def test_convert_videos_no_files(
    mock_video_converter, mock_file_repository, mock_logger, conversion_config
):
    """Test batch conversion when no files are found."""
    use_case = ConvertVideosUseCase(mock_video_converter, mock_file_repository, mock_logger)

    use_case.file_service = MagicMock()
    use_case.file_service.find_videos_in_directories.return_value = []

    results = use_case.execute([Path("test_dir")], conversion_config)

    assert len(results) == 0
