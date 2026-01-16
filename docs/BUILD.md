# Build Guide

## Creating Standalone Executables

Build self-contained executables that run without Python installed.

---

## Prerequisites

Install PyInstaller:

```bash
pip install pyinstaller
```

---

## Quick Build

### Windows

```batch
build_exe.bat
```

Output: `dist\SolverGUI.exe`

### Linux/macOS

```bash
chmod +x build_exe.sh
./build_exe.sh
```

Output: `dist/SolverGUI`

---

## Manual Build

### Basic Build

```bash
pyinstaller --onefile --windowed --name "SolverGUI" main.py
```

**Options:**
- `--onefile`: Single executable file
- `--windowed`: No console window (GUI only)
- `--name "SolverGUI"`: Output filename

### With Icon (Windows)

```bash
pyinstaller --onefile --windowed --name "SolverGUI" --icon=icon.ico main.py
```

### macOS App Bundle

```bash
pyinstaller --onefile --windowed --name "SolverGUI" \
    --osx-bundle-identifier com.solver.gui main.py
```

---

## Build Output

After building:

```
dist/
└── SolverGUI.exe        # Windows executable
    or
    SolverGUI            # Linux/macOS executable
    or  
    SolverGUI.app        # macOS app bundle
```

### File Sizes

Typical sizes:
- **Windows**: ~80-120 MB
- **Linux**: ~90-130 MB
- **macOS**: ~90-130 MB

Size is due to bundled Python interpreter and PySide6 libraries.

---

## Advanced Options

### Reduce File Size (Optional)

Using UPX compression:

```bash
# Install UPX
# Windows: Download from upx.github.io
# Linux: sudo apt install upx
# macOS: brew install upx

# Build with compression
pyinstaller --onefile --windowed --name "SolverGUI" \
    --upx-dir=/path/to/upx main.py
```

### Debug Mode

Build with console window for debugging:

```bash
pyinstaller --onefile --name "SolverGUI" main.py
```

(Remove `--windowed` flag)

---

## Clean Build

Remove old build files before rebuilding:

### Windows
```batch
rmdir /s /q build dist
del SolverGUI.spec
build_exe.bat
```

### Linux/macOS
```bash
rm -rf build dist SolverGUI.spec
./build_exe.sh
```

Or use PyInstaller's clean flag:
```bash
pyinstaller --clean --onefile --windowed --name "SolverGUI" main.py
```

---

## Distribution

### Windows

1. **Single File**
   - Distribute: `dist\SolverGUI.exe`
   - Users double-click to run
   - No installation needed

2. **With Installer** (optional)
   - Use Inno Setup or NSIS
   - Create Windows installer package

### Linux

1. **Executable**
   ```bash
   chmod +x dist/SolverGUI
   ```
   - Distribute: `dist/SolverGUI`
   - Users run: `./SolverGUI`

2. **AppImage** (optional)
   - Package as AppImage for broader compatibility

### macOS

1. **App Bundle**
   - Distribute: `dist/SolverGUI.app`
   - Users drag to Applications folder

2. **DMG** (optional)
   - Create DMG installer with Disk Utility

---

## Troubleshooting Build Issues

### "Module not found" errors

Add hidden imports:
```bash
pyinstaller --onefile --windowed --name "SolverGUI" \
    --hidden-import=PySide6 main.py
```

### Antivirus false positives

- Normal for PyInstaller executables
- Submit to antivirus vendor as false positive
- Sign executable (Windows code signing certificate)

### Build fails on import

Ensure all dependencies are installed:
```bash
pip install -r requirements.txt
pyinstaller --clean --onefile --windowed --name "SolverGUI" main.py
```

### Executable won't start

Test with console mode:
```bash
pyinstaller --onefile --name "SolverGUI_debug" main.py
dist\SolverGUI_debug.exe
```

Check error messages in console.

---

## Automated Builds

### GitHub Actions (CI/CD)

Create `.github/workflows/build.yml`:

```yaml
name: Build Executables

on: [push, pull_request]

jobs:
  build:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [windows-latest, ubuntu-latest, macos-latest]
    
    steps:
    - uses: actions/checkout@v2
    - uses: actions/setup-python@v2
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install pyinstaller
    
    - name: Build executable
      run: pyinstaller --onefile --windowed --name "SolverGUI" main.py
    
    - name: Upload artifact
      uses: actions/upload-artifact@v2
      with:
        name: SolverGUI-${{ matrix.os }}
        path: dist/
```

---

## Build Checklist

Before distributing:

- [ ] Test executable on clean system (no Python installed)
- [ ] Verify all tabs load correctly
- [ ] Test file browsing works
- [ ] Confirm output file generation
- [ ] Check file size is reasonable
- [ ] Test on target platform(s)
- [ ] Include README or usage instructions
- [ ] Version number in filename (optional)

---

## Version Management

Include version in build:

```bash
pyinstaller --onefile --windowed \
    --name "SolverGUI-v2.0" main.py
```

Or edit in code:
```python
# In main.py or trial.py
__version__ = "2.0.0"
self.setWindowTitle(f"Solver GUI v{__version__}")
```

---

## Next Steps

- [Installation Guide](INSTALLATION.md) - How users install/run
- [Customization Guide](CUSTOMIZATION.md) - Modify before building
