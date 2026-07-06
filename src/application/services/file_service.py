"""File discovery service."""

from pathlib import Path

from src.domain.interfaces import IFileRepository, ILogger


class FileDiscoveryService:
    """Service for discovering video files in directories."""

    def __init__(self, file_repository: IFileRepository, logger: ILogger):
        """
        Initialize the file discovery service.

        Args:
            file_repository: File repository implementation
            logger: Logger implementation
        """
        self.file_repository = file_repository
        self.logger = logger

    def find_videos_in_directories(
        self, directories: list[Path], recursive: bool = True
    ) -> list[Path]:
        """
        Find all AVI files in multiple directories.

        Args:
            directories: List of directories to search
            recursive: Whether to search subdirectories

        Returns:
            List of paths to AVI files
        """
        all_files: list[Path] = []

        self.logger.info(f"Starting directory scan for {len(directories)} directories")

        for idx, directory in enumerate(directories, 1):
            self.logger.info(f"Processing directory {idx}/{len(directories)}: {directory}")

            if not directory.exists():
                self.logger.warning(f"Directory does not exist: {directory}")
                continue

            if not directory.is_dir():
                self.logger.warning(f"Path is not a directory: {directory}")
                continue

            self.logger.info(f"Searching for AVI files in: {directory}")
            self.logger.info("This may take a while for directories with many subdirectories...")

            import time

            start_time = time.time()

            files = self.file_repository.find_avi_files(directory, recursive)

            scan_time = time.time() - start_time
            all_files.extend(files)

            self.logger.info(
                f"Found {len(files)} AVI files in {directory} (scan took {scan_time:.1f} seconds)"
            )
            self.logger.info(f"Total files so far: {len(all_files)}")

        self.logger.info(f"Directory scan complete. Total AVI files found: {len(all_files)}")
        return all_files
