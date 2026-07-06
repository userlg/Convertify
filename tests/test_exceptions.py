"""Tests for domain exceptions."""
from src.domain.exceptions import (
    ConvertifyException,
    VideoConversionError,
    FileLockedError,
    InvalidVideoError,
    ConfigurationError,
)

def test_exceptions_inheritance():
    """Test that all exceptions inherit from ConvertifyException."""
    assert issubclass(VideoConversionError, ConvertifyException)
    assert issubclass(FileLockedError, ConvertifyException)
    assert issubclass(InvalidVideoError, ConvertifyException)
    assert issubclass(ConfigurationError, ConvertifyException)

def test_exceptions_initialization():
    """Test instantiating exceptions."""
    err = VideoConversionError("Failed to convert")
    assert str(err) == "Failed to convert"
    
    err = FileLockedError("File is locked")
    assert str(err) == "File is locked"
    
    err = InvalidVideoError("Invalid video")
    assert str(err) == "Invalid video"
    
    err = ConfigurationError("Config error")
    assert str(err) == "Config error"
