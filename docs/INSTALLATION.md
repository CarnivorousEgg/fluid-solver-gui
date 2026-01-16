# Installation Guide

## System Requirements

- **Python**: 3.8 or higher
- **OS**: Windows 10+, Linux, or macOS 10.14+
- **RAM**: 256 MB minimum
- **Disk Space**: 200 MB for Python + dependencies

---

## Installation Steps

### Windows

#### Option 1: Using Python

1. **Install Python**
   - Download from [python.org](https://www.python.org/downloads/)
   - Check "Add Python to PATH" during installation

2. **Install Dependencies**
   ```batch
   pip install PySide6
   ```

3. **Run Application**
   ```batch
   python main.py
   ```

#### Option 2: Using Executable

1. Download `SolverGUI.exe` from releases
2. Double-click to run (no installation needed)

---

### Linux

1. **Install Python** (if not already installed)
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip
   ```

2. **Install Dependencies**
   ```bash
   pip3 install PySide6
   ```

3. **Run Application**
   ```bash
   python3 main.py
   ```

---

### macOS

1. **Install Python** (if not already installed)
   ```bash
   brew install python3
   ```

2. **Install Dependencies**
   ```bash
   pip3 install PySide6
   ```

3. **Run Application**
   ```bash
   python3 main.py
   ```

---

## Virtual Environment (Recommended)

Using a virtual environment keeps dependencies isolated:

### Windows
```batch
python -m venv .venv
.venv\Scripts\activate
pip install PySide6
python main.py
```

### Linux/macOS
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install PySide6
python main.py
```

---

## Installing from requirements.txt

```bash
pip install -r requirements.txt
```

---

## Verifying Installation

Test the installation:

```bash
python -c "from PySide6.QtWidgets import QApplication; print('✓ PySide6 installed correctly')"
```

Expected output:
```
✓ PySide6 installed correctly
```

---

## Troubleshooting Installation

### "python" command not found
- **Windows**: Reinstall Python and check "Add to PATH"
- **Linux/macOS**: Use `python3` instead of `python`

### Permission denied
```bash
# Linux/macOS
pip3 install --user PySide6
```

### PySide6 installation fails
Try upgrading pip first:
```bash
python -m pip install --upgrade pip
pip install PySide6
```

---

## Next Steps

- [Usage Guide](USAGE.md) - Learn how to use the application
- [Build Guide](BUILD.md) - Create standalone executables
