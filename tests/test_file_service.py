"""Tests for file service."""

from pathlib import Path
from unittest.mock import MagicMock

from src.application.services.file_service import FileDiscoveryService


def test_find_videos_in_directories(mock_file_repository, mock_logger):
    """Test finding videos across multiple directories."""
    # Setup mock
    file1 = Path("dir1/video1.avi")
    file2 = Path("dir2/video2.avi")

    # Configure mock to return different files for different directories
    def mock_find_avi(directory, recursive):
        if str(directory) == "dir1":
            return [file1]
        elif str(directory) == "dir2":
            return [file2]
        return []

    mock_file_repository.find_avi_files.side_effect = mock_find_avi

    # Create service
    service = FileDiscoveryService(mock_file_repository, mock_logger)

    # Create test directories (mocking their existence)
    dir1 = MagicMock(spec=Path)
    dir1.exists.return_value = True
    dir1.is_dir.return_value = True
    dir1.__str__.return_value = "dir1"

    dir2 = MagicMock(spec=Path)
    dir2.exists.return_value = True
    dir2.is_dir.return_value = True
    dir2.__str__.return_value = "dir2"

    dir3 = MagicMock(spec=Path)
    dir3.exists.return_value = False

    # Execute
    result = service.find_videos_in_directories([dir1, dir2, dir3])

    # Verify
    assert len(result) == 2
    assert file1 in result
    assert file2 in result
    assert mock_file_repository.find_avi_files.call_count == 2
