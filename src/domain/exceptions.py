"""Custom exceptions for the domain layer."""


class ConvertifyException(Exception):
    """Base exception for all Convertify errors."""

    pass


class VideoConversionError(ConvertifyException):
    """Raised when video conversion fails."""

    pass


class FileLockedError(ConvertifyException):
    """Raised when a file is locked and cannot be accessed."""

    pass


class InvalidVideoError(ConvertifyException):
    """Raised when a video file is invalid or corrupted."""

    pass


class ConfigurationError(ConvertifyException):
    """Raised when configuration is invalid."""

    pass
