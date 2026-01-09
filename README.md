# Convertify 2.0

![Static Badge](https://img.shields.io/badge/Python-3.12-F6D346)
![Static Badge](https://img.shields.io/badge/Architecture-Clean-blue)
![Static Badge](https://img.shields.io/badge/MoviePy-2.1.2-green)
![Static Badge](https://img.shields.io/badge/Status-Production-success)

**Modern AVI to MP4 video converter with Clean Architecture**

Convertify is a professional-grade video conversion tool that automatically converts AVI files to MP4 format with optimized settings. Version 2.0 features a complete architectural redesign using Clean Architecture principles, async processing, and a beautiful CLI interface.

---

## ✨ Features

- 🎯 **Clean Architecture** - Maintainable, testable, and scalable codebase
- ⚡ **High Performance** - Optimized conversion with configurable quality settings
- 🎨 **Beautiful CLI** - Rich terminal interface with progress tracking
- 📝 **Structured Logging** - Comprehensive logging with rotation and retention
- ⚙️ **Flexible Configuration** - Environment-based settings with sensible defaults
- 🔄 **Retry Logic** - Automatic retry for failed conversions
- 🔒 **File Lock Detection** - Skips files currently in use
- 📊 **Detailed Reports** - Conversion statistics and file size comparisons

---

## 📋 Requirements

- **Python 3.12+**
- **Windows OS** (for file lock detection)
- **FFmpeg** (automatically installed with moviepy)

---

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/userlg/Convertify.git
cd Convertify
```

### 2. Create virtual environment

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment

```bash
# Copy example configuration
copy .env.example .env

# Edit .env with your directories
notepad .env
```

---

## 🎯 Usage

### Basic Usage

```bash
# Convert videos in configured directories
python main.py convert

# Specify custom directories
python main.py convert --dir "C:\Videos" --dir "D:\More Videos"

# Keep source files after conversion
python main.py convert --keep-source

# Overwrite existing MP4 files
python main.py convert --overwrite
```

### CLI Options

```bash
Options:
  --dir, -d TEXT              Directories to scan (can be used multiple times)
  --remove-source/--keep-source  Remove source AVI files after conversion
  --skip-existing/--overwrite    Skip if MP4 already exists
  --help                      Show help message
```

### Configuration (.env)

```bash
# Directories to scan (comma-separated)
CONVERSION_DIRECTORIES=Z:/Videos,C:/MyVideos

# Video settings
VIDEO_CODEC=libx264
CRF=23                    # Quality (0-51, lower = better)
PRESET=medium             # Speed preset

# Behavior
REMOVE_SOURCE=true        # Delete AVI after conversion
SKIP_IF_EXISTS=true       # Skip if MP4 exists
MAX_RETRIES=3             # Retry failed conversions

# Performance
MAX_WORKERS=4             # Parallel workers

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/convertify.log
```

---

## 🏗️ Architecture

Convertify 2.0 follows **Clean Architecture** principles:

```
src/
├── domain/              # Business entities and interfaces
│   ├── entities.py      # VideoFile, ConversionResult, ConversionConfig
│   ├── interfaces.py    # IVideoConverter, IFileRepository, ILogger
│   └── exceptions.py    # Custom exceptions
├── infrastructure/      # External dependencies
│   ├── video_converter.py   # MoviePy implementation
│   ├── file_repository.py   # File system operations
│   └── logger.py            # Loguru implementation
├── application/         # Business logic
│   ├── services/
│   │   ├── video_service.py  # Conversion orchestration
│   │   └── file_service.py   # File discovery
│   └── use_cases/
│       └── convert_videos.py # Main use case
├── config.py            # Configuration management
└── container.py         # Dependency injection
```

### Key Benefits

- **Testability**: Easy to mock and test each layer
- **Maintainability**: Clear separation of concerns
- **Scalability**: Easy to add new features
- **Flexibility**: Swap implementations without changing business logic

---

## 🧪 Testing

### Run all tests

```bash
pytest --cov=src --cov-report=html -v
```

### Run specific test file

```bash
pytest tests/test_video_service.py -v
```

### Generate coverage report

```bash
pytest --cov=src --cov-report=html
# Open htmlcov/index.html in browser
```

### Type checking

```bash
mypy src/
```

### Linting

```bash
ruff check src/
```

---

## 📦 Building Executable

Create a standalone executable with PyInstaller:

```bash
pyinstaller --onefile --icon=favicon.ico main.py --name=convertify --collect-all moviepy --collect-all pydantic --collect-all loguru
```

The executable will be in the `dist/` folder.

---

## 📊 Performance

**Improvements in v2.0:**

- ⚡ **Faster startup** - Optimized imports and lazy loading
- 🔄 **Better resource management** - Proper cleanup of video clips
- 📈 **Progress tracking** - Real-time conversion progress
- 🎯 **Smarter file discovery** - Efficient directory traversal
- 💾 **Lower memory usage** - Streaming conversion

---

## 🔧 Development

### Project Structure

```
Convertify/
├── src/                 # Source code
├── tests/               # Test suite
├── logs/                # Log files
├── .env                 # Configuration
├── main.py              # Entry point
├── requirements.txt     # Dependencies
└── pyproject.toml       # Project metadata
```

### Adding New Features

1. Define entities in `domain/entities.py`
2. Create interfaces in `domain/interfaces.py`
3. Implement in `infrastructure/`
4. Add business logic in `application/services/`
5. Create use case in `application/use_cases/`
6. Wire up in `container.py`

---

## 📝 Changelog

### Version 2.0.0 (2026-01-09)

- ✨ Complete architectural redesign with Clean Architecture
- ⚡ Improved performance and resource management
- 🎨 Beautiful CLI with Rich library
- 📝 Structured logging with Loguru
- ⚙️ Environment-based configuration
- 🧪 Comprehensive test suite
- 📊 Detailed conversion reports
- 🔄 Retry logic for failed conversions
- 🔒 File lock detection

### Version 1.0.0

- Initial release with basic conversion functionality

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

MIT License - feel free to use this project for any purpose.

---

## 👤 Author

**userlg**

- GitHub: [@userlg](https://github.com/userlg)

---

## 🙏 Acknowledgments

- [MoviePy](https://github.com/Zulko/moviepy) - Video editing library
- [Typer](https://typer.tiangolo.com/) - CLI framework
- [Rich](https://rich.readthedocs.io/) - Beautiful terminal output
- [Pydantic](https://pydantic-docs.helpmanual.io/) - Data validation
- [Loguru](https://github.com/Delgan/loguru) - Logging made simple

---

**Made with ❤️ by userlg**
