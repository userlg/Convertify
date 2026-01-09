"""File system repository implementation."""

import ctypes
from pathlib import Path

import psutil

from src.domain.interfaces import IFileRepository


class FileSystemRepository(IFileRepository):
    """Implementation of file repository using the file system."""

    def exists(self, file_path: Path) -> bool:
        """Check if a file exists."""
        return file_path.exists()

    def get_file_size(self, file_path: Path) -> int:
        """Get file size in bytes."""
        if not file_path.exists():
            return 0
        return file_path.stat().st_size

    def remove(self, file_path: Path) -> bool:
        """Remove a file."""
        try:
            if file_path.exists():
                file_path.unlink()
                return True
            return False
        except Exception:
            return False

    def is_file_locked(self, file_path: Path) -> bool:
        """
        Check if a file is locked/in use (Windows-specific implementation).

        Uses Windows API to check if file can be opened exclusively.
        """
        if not file_path.exists():
            return False

        # Windows API constants
        GENERIC_READ = 0x80000000
        FILE_SHARE_READ = 0x00000001 | 0x00000002 | 0x00000004
        OPEN_EXISTING = 3
        FILE_ATTRIBUTE_NORMAL = 0x80

        try:
            # Try to open the file with CreateFile
            handle = ctypes.windll.kernel32.CreateFileW(
                str(file_path),
                GENERIC_READ,
                FILE_SHARE_READ,
                None,
                OPEN_EXISTING,
                FILE_ATTRIBUTE_NORMAL,
                None,
            )

            if handle == -1:
                return True  # File is locked

            # Close the handle
            ctypes.windll.kernel32.CloseHandle(handle)

            # Double-check with psutil
            file_lower = str(file_path).lower()
            for proc in psutil.process_iter(["open_files"]):
                try:
                    if proc.info["open_files"]:
                        for f in proc.info["open_files"]:
                            if f.path.lower() == file_lower:
                                return True
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    continue

            return False

        except Exception:
            # If we can't determine, assume it's locked to be safe
            return True

    def find_avi_files(self, directory: Path, recursive: bool = True) -> list[Path]:
        """
        Find all AVI files in a directory.

        Args:
            directory: Directory to search
            recursive: Whether to search subdirectories

        Returns:
            List of paths to AVI files
        """
        if not directory.exists() or not directory.is_dir():
            return []

        avi_files: list[Path] = []

        if recursive:
            # Use rglob for recursive search, excluding hidden directories
            for file_path in directory.rglob("*.avi"):
                # Skip hidden directories (starting with .)
                if not any(part.startswith(".") for part in file_path.parts):
                    avi_files.append(file_path)
        else:
            # Use glob for non-recursive search
            avi_files = list(directory.glob("*.avi"))

        return sorted(avi_files)
