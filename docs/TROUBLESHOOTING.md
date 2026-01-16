# Troubleshooting Guide

Common issues and solutions when working with the Solver GUI.

---

## Installation Issues

### "Module not found: PySide6"

**Problem**: PySide6 not installed

**Solution**:
```powershell
pip install PySide6
```

Or install all dependencies:
```powershell
pip install -r requirements.txt
```

---

### "Python command not found"

**Problem**: Python not in PATH

**Windows Solution**:
1. Reinstall Python with "Add to PATH" checked
2. Or add manually: Search "Environment Variables" → Edit PATH → Add Python folder

**Linux/macOS Solution**:
```bash
# Check if installed
python3 --version

# If not installed
sudo apt install python3 python3-pip  # Ubuntu/Debian
brew install python3                   # macOS
```

---

### Virtual environment activation fails

**Windows**:
```powershell
# If script execution disabled
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then activate
.venv\Scripts\activate
```

**Linux/macOS**:
```bash
# Make sure script is executable
chmod +x .venv/bin/activate

# Then activate
source .venv/bin/activate
```

---

## Runtime Issues

### Application doesn't start

**Check 1**: Verify Python version
```powershell
python --version  # Should be 3.8+
```

**Check 2**: Test imports
```powershell
python -c "from PySide6.QtWidgets import QApplication; print('OK')"
```

**Check 3**: Run with error output
```powershell
python main.py 2>&1 | Tee-Object error.log
```

---

### "Cannot import name 'SolverGUI'"

**Problem**: Import path issue

**Solution**: Make sure you're in correct directory
```powershell
cd "c:\Users\jajoo\OneDrive\Desktop\BITS\vaibhav joshi"
python main.py
```

---

### UI looks broken/unstyled

**Problem**: Stylesheet not loading

**Solution 1**: Check `trial.py` lines 54-67 are not commented out

**Solution 2**: If using modular version, verify `utils/styles.py` exists:
```powershell
python -c "from utils.styles import get_stylesheet; print(len(get_stylesheet()))"
# Should print large number (stylesheet length)
```

---

### Window doesn't open fullscreen

**Problem**: Code modified incorrectly

**Solution**: Check `trial.py` line 46:
```python
self.showMaximized()  # Correct
# NOT self.resize(1250, 850)
```

---

## File Generation Issues

### "No such file or directory" when saving

**Problem**: Invalid path or missing folders

**Solution**:
- Don't include folder path in filename field
- Use absolute paths in coordinate/connectivity file fields
- Browse instead of typing paths manually

---

### Output file is empty

**Problem**: No data entered

**Solution**: Fill all required fields:
1. Geometry tab: Coordinate file, connectivity file, at least 1 boundary
2. Solver tab: All simulation parameters
3. Physical properties tab: Density, viscosity, etc.

---

### Boundary conditions not appearing in output

**Problem**: Tag 0 or empty type

**Solution**:
- Make sure boundary type is selected (not "Select type")
- Check tag number is not 0 (reserved for internal use)
- Verify boundary name is not empty

---

### "Acoustic NRBC parameters missing"

**Problem**: Using LPCE equation without NRBC params

**Solution**: Fill in Solver tab → Acoustic group:
- Centre X, Y, Z coordinates
- Inner radius
- Outer radius

Default values work for testing (0, 0, 0, 1, 2).

---

## Build Issues (PyInstaller)

### "pyinstaller: command not found"

**Problem**: PyInstaller not installed

**Solution**:
```powershell
pip install pyinstaller
```

---

### Build fails with "RecursionError"

**Problem**: PyInstaller recursion limit

**Solution**: Increase recursion limit:
```powershell
pyinstaller --onefile --windowed --name "SolverGUI" --recursion-limit 5000 main.py
```

---

### Executable crashes on startup

**Problem**: Missing dependencies

**Solution**: Check imports in build:
```powershell
pyinstaller --onefile --windowed --name "SolverGUI" --debug all main.py
# Run dist/SolverGUI.exe and check console output
```

Or add hidden imports:
```powershell
pyinstaller --onefile --windowed --hidden-import PySide6.QtCore --hidden-import PySide6.QtWidgets main.py
```

---

### Executable is too large (>100MB)

**Problem**: PyInstaller bundles everything

**Solution 1**: Use `--onefile` instead of `--onedir`

**Solution 2**: Exclude unnecessary modules:
```powershell
pyinstaller --onefile --windowed --exclude-module matplotlib --exclude-module numpy main.py
```

**Note**: Only exclude if you're certain they're not used!

---

### "Cannot find 'main.py'"

**Problem**: Wrong directory

**Solution**: Navigate to project folder first:
```powershell
cd "c:\Users\jajoo\OneDrive\Desktop\BITS\vaibhav joshi"
build_exe.bat
```

---

## Platform-Specific Issues

### Windows: "Script execution is disabled"

**Problem**: PowerShell execution policy

**Solution**:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

### Linux: "Permission denied" when running executable

**Problem**: Executable not marked as executable

**Solution**:
```bash
chmod +x dist/SolverGUI
./dist/SolverGUI
```

---

### macOS: "App is damaged and can't be opened"

**Problem**: Gatekeeper blocking unsigned app

**Solution**:
```bash
xattr -cr dist/SolverGUI.app
```

Or right-click → Open (first time only).

---

## Modular Structure Issues

### "No module named 'utils'"

**Problem**: Missing `__init__.py` files

**Solution**: Create them:
```powershell
# Windows
New-Item -ItemType File -Path "utils\__init__.py"
New-Item -ItemType File -Path "tabs\__init__.py"

# Linux/macOS
touch utils/__init__.py
touch tabs/__init__.py
```

---

### "AttributeError: 'GeometryTab' has no attribute 'X'"

**Problem**: Modular tab missing methods

**Solution**: Compare with `tabs/geometry_tab.py` - ensure all getter methods exist:
- `get_coord_file()`
- `get_conn_file()`
- `get_conn_type()`
- `get_boundary_rows()`

---

## Data Issues

### Boundary labels show "B-2, B-2" instead of "B-2, B-3"

**Problem**: Old version of code

**Solution**: Update to latest `trial.py` - should have `_refresh_bc_labels()` method around line 629.

---

### Acoustic parameters not in output file

**Problem**: Old version missing acoustic support

**Solution**: Check `trial.py` line 182 - should have "LPCE" in combo box options.

---

### Initial psi field missing

**Problem**: Old version without psi support

**Solution**: Check `trial.py` line 493 - should create `init_cond_widgets['psi']`.

---

## Performance Issues

### Application starts slowly

**Cause**: Normal for Python GUI applications

**Solution**: Use built executable for faster startup:
```powershell
.\dist\SolverGUI.exe
```

---

### Scrolling is laggy with many boundaries

**Cause**: Many widgets in scroll area

**Solution**: This is expected with 50+ boundaries. Performance is adequate for typical use (10-20 boundaries).

---

## Debug Mode

### Enable detailed error messages

Run with traceback:
```powershell
python -u main.py
```

---

### Check widget values

Add temporary debug code:
```python
# In save_input_file(), before writing
print(f"Coordinate file: {self.coord_edit.text()}")
print(f"Connectivity file: {self.conn_edit.text()}")
print(f"Boundaries: {len(self.geometry_boundary_rows)}")
```

---

### Verify imports

```powershell
python -c "import sys; print(sys.path)"
python -c "from trial import SolverGUI; print('✓ Import successful')"
```

---

## Getting Help

### Still having issues?

1. **Check error message**: Read the full error - often tells you exactly what's wrong
2. **Check file paths**: Make sure paths don't have special characters
3. **Restart application**: Close and reopen
4. **Reinstall dependencies**: `pip install --force-reinstall -r requirements.txt`
5. **Try fresh virtual environment**: See [Installation Guide](INSTALLATION.md)

### Report a bug

Include:
- Error message (full traceback)
- Steps to reproduce
- Python version: `python --version`
- PySide6 version: `pip show PySide6`
- Operating system

---

## Quick Fixes Summary

| Issue | Quick Fix |
|-------|-----------|
| Module not found | `pip install -r requirements.txt` |
| Can't run script | `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser` |
| Import error | `cd` to correct directory |
| UI broken | Check stylesheet not commented out |
| Empty output | Fill all required fields |
| Build fails | `pip install pyinstaller` |
| Exe crashes | Add `--debug all` flag |

---

**Related Documents**:
- [Installation](INSTALLATION.md) - Setup instructions
- [Usage](USAGE.md) - How to use the application
- [Build Guide](BUILD.md) - Creating executables
