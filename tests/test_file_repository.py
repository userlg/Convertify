"""Tests for file repository."""

from pathlib import Path

from src.infrastructure.file_repository import FileSystemRepository


def test_file_exists(temp_dir):
    """Test file exists check."""
    repo = FileSystemRepository()

    # Create a file
    test_file = temp_dir / "test.txt"
    test_file.write_text("content")

    assert repo.exists(test_file) is True
    assert repo.exists(temp_dir / "nonexistent.txt") is False


def test_get_file_size(temp_dir):
    """Test getting file size."""
    repo = FileSystemRepository()

    test_file = temp_dir / "test.txt"
    content = "test content"
    test_file.write_text(content)

    assert repo.get_file_size(test_file) == len(content)
    assert repo.get_file_size(temp_dir / "nonexistent.txt") == 0


def test_remove_file(temp_dir):
    """Test file removal."""
    repo = FileSystemRepository()

    test_file = temp_dir / "test.txt"
    test_file.write_text("content")

    assert repo.remove(test_file) is True
    assert not test_file.exists()
    assert repo.remove(test_file) is False  # Already removed


def test_find_avi_files(temp_dir):
    """Test finding AVI files."""
    repo = FileSystemRepository()

    # Create test structure
    (temp_dir / "video1.avi").write_text("fake")
    (temp_dir / "video2.avi").write_text("fake")
    (temp_dir / "video.mp4").write_text("fake")

    subdir = temp_dir / "subdir"
    subdir.mkdir()
    (subdir / "video3.avi").write_text("fake")

    # Test recursive search
    files = repo.find_avi_files(temp_dir, recursive=True)
    assert len(files) == 3
    assert all(f.suffix == ".avi" for f in files)

    # Test non-recursive search
    files = repo.find_avi_files(temp_dir, recursive=False)
    assert len(files) == 2


def test_find_avi_files_excludes_hidden(temp_dir):
    """Test that hidden directories are excluded."""
    repo = FileSystemRepository()

    # Create hidden directory
    hidden_dir = temp_dir / ".hidden"
    hidden_dir.mkdir()
    (hidden_dir / "video.avi").write_text("fake")

    files = repo.find_avi_files(temp_dir, recursive=True)
    assert len(files) == 0


def test_is_file_locked_nonexistent():
    """Test file locked check for nonexistent file."""
    repo = FileSystemRepository()
    assert repo.is_file_locked(Path("nonexistent.txt")) is False
