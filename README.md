# Convertify 2.0 (Background Service Edition)

![Static Badge](https://img.shields.io/badge/Python-3.13-F6D346)
![Static Badge](https://img.shields.io/badge/Architecture-Clean-blue)
![Static Badge](https://img.shields.io/badge/FFmpeg-Stream_Copy-green)
![Static Badge](https://img.shields.io/badge/Status-Production-success)

**Instantaneous AVI to MP4 background converter for Windows**

Convertify is a streamlined, zero-configuration background service designed to automatically monitor network directories and instantly wrap `.avi` files into `.mp4` containers.

---

## ✨ Features

- 🎯 **Clean Architecture** - Maintainable, testable, and scalable codebase.
- ⚡ **Instant Conversion (Stream Copy)** - Bypasses slow re-encoding completely by copying the video and audio streams directly into an MP4 container.
- 🏢 **Hardcoded Network Paths** - Direct IP-based UNC paths (`\\192.168.1.200`) prevent DNS resolution drops in background services.
- 👻 **Zero-Argument Background Execution** - No CLI, no menus, no prompts. The executable is built to run silently in the background.
- 🧠 **Intelligent Caching** - Scans only new/modified directories to handle massive network structures in seconds.
- 📝 **Hidden Logging** - Comprehensive standard logging with automatic hidden folder creation.
- 🔒 **File Lock Detection** - Safely skips files currently in use by other processes.

---

## 📋 Requirements

- **Python 3.13+** (for development)
- **Windows OS** (designed specifically for Windows environments and services)

---

## 🚀 Execution

The tool is designed to be executed as a compiled executable (`.exe`). Since it takes zero arguments, it can be launched directly or invoked via a silent `.vbs` wrapper.

**VBS Production Script** (`convertify.vbs`):

```vbscript
' Silent execution for automated workflows
Set objShell = CreateObject("WScript.Shell")
Set objFSO = CreateObject("Scripting.FileSystemObject")
scriptDir = objFSO.GetParentFolderName(WScript.ScriptFullName)
objShell.CurrentDirectory = scriptDir
exePath = scriptDir & "\convertify.exe"
' No arguments needed
objShell.Run """" & exePath & """", 0, True
```

This automatically processes the predefined directories:
- `\\192.168.1.200\Team-design\4. PREPARAR RESUMEN`
- `\\192.168.1.200\Team-design\8. Base Datos Unica`

---

## 💻 Development Setup

### 1. Clone & Setup

```bash
git clone https://github.com/userlg/Convertify.git
cd Convertify
python -m venv .venv
.\.venv\Scripts\activate
```

### 2. Install Dependencies

```bash
# Install with development tools
pip install -e .[dev]
```

---

## 🏗️ Architecture

Convertify follows Clean Architecture principles:

```
src/
├── domain/          # Business logic, entities, and interfaces
├── application/     # Use cases and services
├── infrastructure/  # External implementations (FFmpeg, File System, Logger)
├── config.py        # Configuration management
└── container.py     # Dependency injection
```

### Key Design Decisions (V2 Background Service)
1. **Instant Stream Copy**: Uses `codec="copy"` to wrap AVI into MP4 instantly without CPU-intensive encoding.
2. **No .env required**: Standalone executable design prevents pathing issues with `.env` files in background services.
3. **No CLI UI**: Removed `typer` and `rich` to prevent terminal output issues and keep the executable as lean as possible.

---

## 🧪 Testing

```bash
# Run all tests
python -m pytest
```

---

## 📦 Building Executable

To generate the standalone executable for Windows, run the following command exactly as shown:

```bash
pyinstaller --onefile --icon=favicon.ico --collect-all moviepy --name convertify main.py --clean
```

Output will be located at: `dist/convertify.exe`

---

## 📄 License
This project is licensed under the MIT License.

## 👤 Author
**userlg**
