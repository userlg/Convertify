"""File system repository implementation."""

import ctypes
from pathlib import Path

import psutil

from src.domain.interfaces import IFileRepository
from src.infrastructure.directory_cache import DirectoryCache


class FileSystemRepository(IFileRepository):
    """Implementation of file repository using the file system with caching."""

    def __init__(self, use_cache: bool = True):
        """
        Initialize file repository.

        Args:
            use_cache: Whether to use directory caching for large directories
        """
        self.use_cache = use_cache
        self.cache = DirectoryCache() if use_cache else None

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
        Find all AVI files in a directory with intelligent caching.

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
            # Check if this is a large directory that would benefit from caching
            use_smart_scan = self.use_cache and self.cache is not None

            if use_smart_scan:
                # Get cache stats
                stats = self.cache.get_cache_stats(directory)
                _ = stats

                # Get directories that need scanning
                dirs_to_scan = self.cache.get_directories_to_scan(directory)

                if not dirs_to_scan:
                    return []

                # Keep branching behavior for cache; no stdout.
                _ = len(dirs_to_scan)

            # Perform the scan
            try:
                if use_smart_scan:
                    # If cache tells us which subdirs to scan, only scan those.
                    # This avoids doing directory-wide rglob over very large trees.
                    if not dirs_to_scan:
                        return []

                    # If cache indicates we need a full scan (e.g., first time / stale cache),
                    # fall back to scanning the whole directory.
                    if directory in dirs_to_scan or len(dirs_to_scan) == 1:
                        scan_roots = [directory]
                    else:
                        scan_roots = list(dirs_to_scan)
                else:
                    scan_roots = [directory]

                for scan_root in scan_roots:
                    for file_path in scan_root.rglob("*.avi"):
                        # Skip hidden directories (starting with .)
                        if not any(part.startswith(".") for part in file_path.parts):
                            avi_files.append(file_path)

                # Update cache after successful scan
                if use_smart_scan:
                    self.cache.update_cache(directory, avi_files)

            except Exception:
                return []

        else:
            # Use glob for non-recursive search
            avi_files = list(directory.glob("*.avi"))

        return sorted(avi_files)
