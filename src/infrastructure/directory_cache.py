"""
Directory cache system for fast scanning of large directory structures.

This module implements a caching system that tracks which directories have been
scanned and only rescans new or modified directories. This is critical for
directories with 900+ subdirectories that are constantly growing.
"""

import json
import time
from pathlib import Path
from typing import Dict, Set


class DirectoryCache:
    """Cache for tracking scanned directories and their modification times."""

    def __init__(self, cache_file: Path | None = None):
        """
        Initialize the directory cache.

        Args:
            cache_file: Path to cache file. If None, uses default location.
        """
        if cache_file is None:
            cache_file = Path("cache/directory_cache.json")
        
        self.cache_file = cache_file
        self.cache_file.parent.mkdir(parents=True, exist_ok=True)
        self.cache: Dict[str, Dict] = self._load_cache()

    def _load_cache(self) -> Dict[str, Dict]:
        """Load cache from file."""
        if not self.cache_file.exists():
            return {}
        
        try:
            with open(self.cache_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return {}

    def _save_cache(self) -> None:
        """Save cache to file."""
        try:
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(self.cache, f, indent=2)
        except Exception:
            pass  # Ignore cache save errors

    def get_directories_to_scan(self, root_dir: Path) -> Set[Path]:
        """
        Get list of directories that need to be scanned.

        Returns only new or modified directories since last scan.

        Args:
            root_dir: Root directory to scan

        Returns:
            Set of directories that need scanning
        """
        if not root_dir.exists():
            return set()

        root_str = str(root_dir)
        dirs_to_scan: Set[Path] = set()
        current_subdirs: Set[str] = set()

        # Get all current subdirectories
        try:
            for item in root_dir.rglob("*"):
                if item.is_dir() and not any(part.startswith(".") for part in item.parts):
                    current_subdirs.add(str(item))
        except Exception:
            # If we can't scan, return root dir to force full scan
            return {root_dir}

        # Check cache for this root directory
        if root_str not in self.cache:
            # First time scanning this root - scan everything
            self.cache[root_str] = {
                "last_scan": time.time(),
                "subdirs": {}
            }
            return {root_dir}  # Full scan

        cached_subdirs = self.cache[root_str].get("subdirs", {})

        # Find new directories (not in cache)
        for subdir_str in current_subdirs:
            if subdir_str not in cached_subdirs:
                dirs_to_scan.add(Path(subdir_str))

        # Find modified directories (mtime changed)
        for subdir_str in current_subdirs:
            if subdir_str in cached_subdirs:
                try:
                    subdir = Path(subdir_str)
                    current_mtime = subdir.stat().st_mtime
                    cached_mtime = cached_subdirs[subdir_str].get("mtime", 0)
                    
                    if current_mtime > cached_mtime:
                        dirs_to_scan.add(subdir)
                except Exception:
                    # If we can't check, add to scan list
                    dirs_to_scan.add(Path(subdir_str))

        # If no specific directories to scan, but cache is old (>1 hour), do full scan
        last_scan = self.cache[root_str].get("last_scan", 0)
        if not dirs_to_scan and (time.time() - last_scan) > 3600:
            return {root_dir}

        return dirs_to_scan if dirs_to_scan else set()

    def update_cache(self, root_dir: Path, scanned_files: list[Path]) -> None:
        """
        Update cache after scanning.

        Args:
            root_dir: Root directory that was scanned
            scanned_files: List of files found during scan
        """
        root_str = str(root_dir)
        
        if root_str not in self.cache:
            self.cache[root_str] = {"subdirs": {}}

        # Update last scan time
        self.cache[root_str]["last_scan"] = time.time()

        # Update subdirectory mtimes
        subdirs_seen: Set[str] = set()
        
        for file_path in scanned_files:
            # Track all parent directories of found files
            current = file_path.parent
            while current != root_dir and current not in subdirs_seen:
                subdir_str = str(current)
                subdirs_seen.add(subdir_str)
                
                try:
                    mtime = current.stat().st_mtime
                    self.cache[root_str]["subdirs"][subdir_str] = {
                        "mtime": mtime,
                        "last_checked": time.time()
                    }
                except Exception:
                    pass
                
                current = current.parent

        self._save_cache()

    def clear_cache(self, root_dir: Path | None = None) -> None:
        """
        Clear cache for a specific directory or all directories.

        Args:
            root_dir: Directory to clear cache for. If None, clears all.
        """
        if root_dir is None:
            self.cache = {}
        else:
            root_str = str(root_dir)
            if root_str in self.cache:
                del self.cache[root_str]
        
        self._save_cache()

    def get_cache_stats(self, root_dir: Path) -> Dict:
        """
        Get statistics about the cache for a directory.

        Args:
            root_dir: Root directory

        Returns:
            Dictionary with cache statistics
        """
        root_str = str(root_dir)
        
        if root_str not in self.cache:
            return {
                "cached": False,
                "subdirs_cached": 0,
                "last_scan": None
            }

        cache_data = self.cache[root_str]
        last_scan = cache_data.get("last_scan", 0)
        
        return {
            "cached": True,
            "subdirs_cached": len(cache_data.get("subdirs", {})),
            "last_scan": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(last_scan)) if last_scan else None,
            "age_hours": (time.time() - last_scan) / 3600 if last_scan else None
        }
