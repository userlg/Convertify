"""
Diagnostic script to test lab directory processing.
Run this to see exactly what's happening with both directories.
"""

from pathlib import Path
from src.config import load_settings

def test_lab_directories():
    print("=" * 80)
    print("CONVERTIFY LAB DIRECTORIES DIAGNOSTIC")
    print("=" * 80)
    
    # Test 1: Load settings and check directories
    print("\n1. Loading settings...")
    settings = load_settings()
    
    # Simulate lab mode
    settings.conversion_directories = [
        r"\\TNAS-Click\Team-design\4. PREPARAR RESUMEN",
        r"\\TNAS-Click\Team-design\8. Base Datos Unica"
    ]
    
    print(f"   Configured directories: {len(settings.conversion_directories)}")
    for i, dir_str in enumerate(settings.conversion_directories, 1):
        print(f"   {i}. {dir_str}")
    
    # Test 2: Convert to Path objects
    print("\n2. Converting to Path objects...")
    dirs = settings.get_conversion_directories()
    print(f"   Path objects created: {len(dirs)}")
    for i, dir_path in enumerate(dirs, 1):
        print(f"   {i}. {dir_path}")
        print(f"      Type: {type(dir_path)}")
        print(f"      Exists: {dir_path.exists()}")
        print(f"      Is directory: {dir_path.is_dir() if dir_path.exists() else 'N/A'}")
    
    # Test 3: Search for AVI files
    print("\n3. Searching for AVI files...")
    from src.infrastructure.file_repository import FileSystemRepository
    from src.infrastructure.logger import LoguruLogger
    from src.application.services.file_service import FileDiscoveryService
    
    logger = LoguruLogger(log_level="DEBUG")
    file_repo = FileSystemRepository()
    file_service = FileDiscoveryService(file_repo, logger)
    
    for i, directory in enumerate(dirs, 1):
        print(f"\n   Directory {i}: {directory}")
        if not directory.exists():
            print(f"   ❌ ERROR: Directory does not exist!")
            continue
        
        if not directory.is_dir():
            print(f"   ❌ ERROR: Path is not a directory!")
            continue
        
        print(f"   ✓ Directory exists and is valid")
        
        # Find AVI files
        avi_files = file_repo.find_avi_files(directory, recursive=True)
        print(f"   Found {len(avi_files)} AVI files")
        
        if avi_files:
            print(f"   First 5 files:")
            for j, file_path in enumerate(avi_files[:5], 1):
                print(f"      {j}. {file_path.name}")
    
    # Test 4: Full discovery
    print("\n4. Running full file discovery...")
    all_files = file_service.find_videos_in_directories(dirs)
    print(f"   Total AVI files found across all directories: {len(all_files)}")
    
    print("\n" + "=" * 80)
    print("DIAGNOSTIC COMPLETE")
    print("=" * 80)

if __name__ == "__main__":
    test_lab_directories()
