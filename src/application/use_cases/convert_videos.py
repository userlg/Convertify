"""Convert videos use case with async processing."""

from collections.abc import Callable
from pathlib import Path

from src.application.services.file_service import FileDiscoveryService
from src.application.services.video_service import VideoConversionService
from src.domain.entities import ConversionConfig, ConversionResult
from src.domain.interfaces import IFileRepository, ILogger, IVideoConverter


class ConvertVideosUseCase:
    """Use case for batch video conversion with async processing."""

    def __init__(
        self,
        converter: IVideoConverter,
        file_repository: IFileRepository,
        logger: ILogger,
        max_workers: int = 4,
    ):
        """
        Initialize the use case.

        Args:
            converter: Video converter implementation
            file_repository: File repository implementation
            logger: Logger implementation
            max_workers: Maximum number of parallel workers
        """
        self.video_service = VideoConversionService(converter, file_repository, logger)
        self.file_service = FileDiscoveryService(file_repository, logger)
        self.logger = logger
        self.max_workers = max_workers

    def execute(
        self,
        directories: list[Path],
        config: ConversionConfig,
        progress_callback: Callable[[int, int], None] | None = None,
    ) -> list[ConversionResult]:
        """
        Execute batch video conversion.

        Args:
            directories: List of directories to search for videos
            config: Conversion configuration
            progress_callback: Optional callback for progress updates (current, total)

        Returns:
            List of conversion results
        """
        self.logger.info(f"Starting batch conversion for {len(directories)} directories")

        # Discover all video files
        video_paths = self.file_service.find_videos_in_directories(directories)

        if not video_paths:
            self.logger.warning("No AVI files found to convert")
            return []

        # Create VideoFile entities
        video_files = [self.video_service.create_video_file(path) for path in video_paths]

        self.logger.info(f"Converting {len(video_files)} videos with {self.max_workers} workers")

        # Convert videos with progress tracking
        results: list[ConversionResult] = []
        total = len(video_files)

        # Parallel conversion (safe because each task runs an external ffmpeg subprocess
        # and we don't share mutable state in the worker beyond read-only services).
        #
        # Note: We intentionally use ThreadPoolExecutor (not ProcessPoolExecutor) because
        # movie/ffmpeg invocation is largely I/O + subprocess-bound and ProcessPool would
        # require picklable callables/objects (often problematic on Windows).
        from concurrent.futures import ThreadPoolExecutor, as_completed

        max_workers = max(1, self.max_workers)
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {
                executor.submit(self.video_service.convert_video, video_file, config): idx
                for idx, video_file in enumerate(video_files, start=1)
            }

            # Preserve deterministic ordering in `results` by collecting with index
            ordered: dict[int, ConversionResult] = {}

            for future in as_completed(futures):
                idx = futures[future]
                try:
                    ordered[idx] = future.result()
                except Exception as e:
                    # Should not happen often (VideoConversionService already catches),
                    # but ensure one task failure doesn't stop the batch.
                    video_file = video_files[idx - 1]
                    ordered[idx] = ConversionResult(
                        video_file=video_file,
                        success=False,
                        error_message=f"Unexpected conversion error: {e}",
                        duration_seconds=0.0,
                    )

                if progress_callback:
                    progress_callback(idx, total)

            results = [ordered[i] for i in range(1, total + 1)]

        # Summary
        successful = sum(1 for r in results if r.success)
        failed = sum(1 for r in results if not r.success)

        self.logger.info(f"Batch conversion complete: {successful} successful, {failed} failed")

        return results
