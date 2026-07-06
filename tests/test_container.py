"""Tests for DI container."""

from src.container import Container
from src.domain.entities import ConversionConfig


def test_container_singletons():
    """Test that container properties return singletons."""
    container = Container()

    logger1 = container.logger
    logger2 = container.logger
    assert logger1 is logger2

    repo1 = container.file_repository
    repo2 = container.file_repository
    assert repo1 is repo2

    converter1 = container.video_converter
    converter2 = container.video_converter
    assert converter1 is converter2

    use_case1 = container.convert_videos_use_case
    use_case2 = container.convert_videos_use_case
    assert use_case1 is use_case2


def test_get_conversion_config():
    """Test get config."""
    container = Container()
    config = container.get_conversion_config()
    assert isinstance(config, ConversionConfig)
    assert config.codec == "copy"
