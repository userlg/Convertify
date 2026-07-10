"""Main entry point for Convertify video converter."""

import sys
from pathlib import Path

from src.container import Container


def main():
    """Convert AVI videos to MP4 format."""
    container: Container | None = None
    try:
        dirs = [
            Path(r"\\192.168.1.200\Team-design\4. PREPARAR RESUMEN"),
            Path(r"\\192.168.1.200\Team-design\8. Base Datos Unica"),
        ]

        # Initialize container
        container = Container()
        config = container.get_conversion_config()
        logger = container.logger

        logger.info("Starting Convertify - AVI to MP4 Converter")
        logger.info(f"Directories to process: {len(dirs)}")
        for idx, d in enumerate(dirs, 1):
            logger.info(f"  {idx}. {d}")

        logger.info(f"Codec: {config.codec}")
        logger.info(f"Remove source: {config.remove_source}")
        logger.info(f"Skip existing: {config.skip_if_exists}")

        # Execute conversion
        use_case = container.convert_videos_use_case
        results = use_case.execute(dirs, config)

        if results:
            successful = sum(1 for r in results if r.video_file.status.value == "completed")
            failed = sum(1 for r in results if r.video_file.status.value == "failed")
            total_time = sum(r.duration_seconds for r in results)

            logger.info(
                f"Completed: {successful} successful, "
                f"{failed} failed, Total time: {total_time:.1f}s"
            )
            for r in results:
                status = "Success" if r.success else "Failed"
                logger.info(
                    f"[{status}] {r.video_file.filename} in {r.duration_seconds:.1f}s"
                )
        else:
            logger.info("No AVI files found to convert.")

    except Exception as e:
        # Ensure background/service failures are logged with traceback
        try:
            logger = container.logger if container else None
            if logger:
                logger.exception(f"Convertify crashed: {str(e)}")
        except Exception:
            # Fallback: no logger available
            pass
        sys.exit(1)


if __name__ == "__main__":
    main()
