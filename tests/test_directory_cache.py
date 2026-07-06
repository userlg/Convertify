"""Tests for directory cache."""

import json

from src.infrastructure.directory_cache import DirectoryCache


def test_directory_cache_init(temp_dir):
    """Test initialization."""
    cache_file = temp_dir / "cache.json"
    cache = DirectoryCache(cache_file)
    assert cache.cache_file == cache_file
    assert cache.cache == {}


def test_directory_cache_load_save(temp_dir):
    """Test loading and saving cache."""
    cache_file = temp_dir / "cache.json"

    # Save manually
    data = {"test": {"last_scan": 123}}
    cache_file.write_text(json.dumps(data))

    # Load
    cache = DirectoryCache(cache_file)
    assert "test" in cache.cache

    # Update and save
    cache.cache["test2"] = {"last_scan": 456}
    cache._save_cache()

    # Verify save
    cache2 = DirectoryCache(cache_file)
    assert "test2" in cache2.cache


def test_get_directories_to_scan(temp_dir):
    """Test directory scanning logic."""
    cache = DirectoryCache(temp_dir / "cache.json")

    # Create structure
    sub1 = temp_dir / "sub1"
    sub1.mkdir()

    # First scan
    to_scan = cache.get_directories_to_scan(temp_dir)
    assert temp_dir in to_scan  # Full scan

    # Update cache
    cache.update_cache(temp_dir, [sub1 / "video.avi"])

    # Second scan, no changes
    to_scan2 = cache.get_directories_to_scan(temp_dir)
    assert len(to_scan2) == 0

    # Add new dir
    sub2 = temp_dir / "sub2"
    sub2.mkdir()

    to_scan3 = cache.get_directories_to_scan(temp_dir)
    assert sub2 in to_scan3


def test_clear_cache(temp_dir):
    """Test clearing cache."""
    cache = DirectoryCache(temp_dir / "cache.json")
    cache.update_cache(temp_dir, [])
    assert str(temp_dir) in cache.cache

    cache.clear_cache(temp_dir)
    assert str(temp_dir) not in cache.cache

    cache.update_cache(temp_dir, [])
    cache.clear_cache()
    assert len(cache.cache) == 0


def test_get_cache_stats(temp_dir):
    """Test getting cache statistics."""
    cache = DirectoryCache(temp_dir / "cache.json")
    stats = cache.get_cache_stats(temp_dir)
    assert stats["cached"] is False

    cache.update_cache(temp_dir, [])
    stats2 = cache.get_cache_stats(temp_dir)
    assert stats2["cached"] is True
