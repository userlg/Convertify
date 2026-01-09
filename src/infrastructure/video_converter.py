"""Video converter implementation using MoviePy."""

import contextlib
import time
from pathlib import Path

from moviepy import VideoFileClip

from src.domain.entities import ConversionConfig, ConversionResult, VideoFile
from src.domain.interfaces import IVideoConverter


class MoviePyVideoConverter(IVideoConverter):
    """Video converter implementation using MoviePy library."""

    def convert(self, video_file: VideoFile, config: ConversionConfig) -> ConversionResult:
        """
        Convert a video file to MP4 format.

        Args:
            video_file: The video file to convert
            config: Conversion configuration

        Returns:
            ConversionResult with success status and details
        """
        start_time = time.time()
        output_path = video_file.get_output_path()

        # Check if output already exists and skip if configured
        if config.skip_if_exists and output_path.exists():
            return ConversionResult(
                video_file=video_file,
                success=True,
                output_path=output_path,
                error_message="Output file already exists, skipped",
                duration_seconds=0.0,
            )

        clip = None
        try:
            # Load the video
            clip = VideoFileClip(str(video_file.path))

            # Convert to MP4 with specified settings
            clip.write_videofile(
                str(output_path),
                codec=config.codec,
                audio_codec=config.audio_codec,
                preset=config.preset,
                ffmpeg_params=["-crf", str(config.crf)],
                audio_bitrate=config.audio_bitrate,
                threads=config.threads if config.threads > 0 else None,
                logger=None,  # Suppress moviepy's default logger
            )

            # Get file sizes
            original_size = video_file.path.stat().st_size / (1024 * 1024)
            converted_size = output_path.stat().st_size / (1024 * 1024)

            duration = time.time() - start_time

            return ConversionResult(
                video_file=video_file,
                success=True,
                output_path=output_path,
                duration_seconds=duration,
                original_size_mb=original_size,
                converted_size_mb=converted_size,
            )

        except Exception as e:
            error_msg = f"Failed to convert {video_file.filename}: {str(e)}"
            return ConversionResult(
                video_file=video_file,
                success=False,
                error_message=error_msg,
                duration_seconds=time.time() - start_time,
            )

        finally:
            # Always close the clip to free resources
            if clip is not None:
                with contextlib.suppress(Exception):
                    clip.close()

    def is_valid_video(self, file_path: Path) -> bool:
        """
        Check if a file is a valid video.

        Args:
            file_path: Path to the video file

        Returns:
            True if valid video, False otherwise
        """
        if not file_path.exists():
            return False

        # Check extension
        if file_path.suffix.lower() not in [".avi", ".mp4", ".mov", ".mkv"]:
            return False

        # Try to open with MoviePy
        clip = None
        try:
            clip = VideoFileClip(str(file_path))
            return clip.duration is not None and clip.duration > 0
        except Exception:
            return False
        finally:
            if clip is not None:
                with contextlib.suppress(Exception):
                    clip.close()
