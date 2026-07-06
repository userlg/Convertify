"""Main entry point for Convertify video converter."""

import argparse
import sys
from pathlib import Path

from src.config import load_settings
from src.container import Container


def main():
    """Convert AVI videos to MP4 format."""
    parser = argparse.ArgumentParser(description="Convert AVI videos to MP4 format automatically")
    parser.add_argument(
        "command",
        nargs="?",
        default="convert",
        help="Command (ignored, for backwards compatibility)",
    )
    parser.add_argument("--dir", "-d", action="append", help="Directories to scan for AVI files")
    parser.add_argument("--lab", action="store_true", help="Use predefined lab directories")
    parser.add_argument("--remove-source", action="store_true", default=None)
    parser.add_argument("--keep-source", action="store_false", dest="remove_source")
    parser.add_argument("--skip-existing", action="store_true", default=None)
    parser.add_argument("--overwrite", action="store_false", dest="skip_existing")

    args = parser.parse_args()

    try:
        # Load settings
        settings = load_settings()

        # Override settings with CLI arguments if provided
        if args.lab:
            settings.conversion_directories = [
                r"\\192.168.1.200\Team-design\4. PREPARAR RESUMEN",
                r"\\192.168.1.200\Team-design\8. Base Datos Unica",
            ]
        elif args.dir:
            settings.conversion_directories = args.dir

        if args.remove_source is not None:
            settings.remove_source = args.remove_source
        if args.skip_existing is not None:
            settings.skip_if_exists = args.skip_existing

        # Validate directories
        dirs = settings.get_conversion_directories()
        if not dirs:
            # Use current directory as default
            dirs = [Path(".")]

        # Initialize container
        container = Container(settings)
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
            successful = sum(1 for r in results if r.success)
            failed = sum(1 for r in results if not r.success)
            total_time = sum(r.duration_seconds for r in results)

            logger.info(
                f"Completed: {successful} successful, "
                f"{failed} failed, Total time: {total_time:.1f}s"
            )
            for r in results:
                status = "Success" if r.success else "Failed"
                logger.info(f"[{status}] {r.video_file.filename} in {r.duration_seconds:.1f}s")
        else:
            logger.info("No AVI files found to convert.")

    except Exception:
        sys.exit(1)


if __name__ == "__main__":
    main()
