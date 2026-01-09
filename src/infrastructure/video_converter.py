"""Video converter implementation using FFmpeg directly for maximum speed."""

import subprocess
import time
from pathlib import Path

import imageio_ffmpeg as ffmpeg

from src.domain.entities import ConversionConfig, ConversionResult, VideoFile
from src.domain.interfaces import IVideoConverter


class MoviePyVideoConverter(IVideoConverter):
    """Video converter using direct FFmpeg for maximum performance."""

    def convert(self, video_file: VideoFile, config: ConversionConfig) -> ConversionResult:
        """
        Convert a video file to MP4 format using FFmpeg directly.

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

        try:
            # Get ffmpeg executable path
            ffmpeg_exe = ffmpeg.get_ffmpeg_exe()

            # Build ffmpeg command for extreme speed
            cmd = [
                ffmpeg_exe,
                "-i", str(video_file.path),  # Input file
                "-c:v", config.codec,  # Video codec
                "-preset", config.preset,  # Encoding preset (ultrafast)
                "-crf", str(config.crf),  # Quality
                "-tune", "fastdecode",  # Optimize for fast decoding
            ]

            # Handle audio codec - copy if specified, otherwise encode
            if config.audio_codec.lower() == "copy":
                cmd.extend(["-c:a", "copy"])  # Copy audio stream without re-encoding
            else:
                cmd.extend([
                    "-c:a", config.audio_codec,  # Audio codec
                    "-b:a", config.audio_bitrate,  # Audio bitrate
                ])

            # Add optimization flags
            cmd.extend([
                "-movflags", "+faststart",  # Optimize for streaming
                "-y",  # Overwrite output
                str(output_path)  # Output file
            ])

            # Add threads if specified (insert after ffmpeg_exe)
            if config.threads > 0:
                cmd.insert(1, "-threads")
                cmd.insert(2, str(config.threads))

            # Run ffmpeg conversion
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=False
            )

            if result.returncode != 0:
                error_msg = f"FFmpeg error: {result.stderr}"
                return ConversionResult(
                    video_file=video_file,
                    success=False,
                    error_message=error_msg,
                    duration_seconds=time.time() - start_time,
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

    def is_valid_video(self, file_path: Path) -> bool:
        """
        Check if a file is a valid video using FFmpeg probe.

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

        try:
            # Use ffmpeg to probe the file
            ffmpeg_exe = ffmpeg.get_ffmpeg_exe()
            cmd = [
                ffmpeg_exe,
                "-v", "error",
                "-i", str(file_path),
                "-f", "null",
                "-"
            ]

            result = subprocess.run(
                cmd,
                capture_output=True,
                timeout=5
            )

            # If ffmpeg can read it without error, it's valid
            return result.returncode == 0

        except Exception:
            return False
