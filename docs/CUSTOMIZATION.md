# Quick Customization Reference

## Most Common Changes

### 1. Change Window Title
**File**: `main.py`, Line 42
```python
self.setWindowTitle("Your New Title Here")
```

### 2. Change Button Colors
**File**: `utils/styles.py`, Lines 15-25
```python
QPushButton { 
    background-color: #YOUR_COLOR;  # e.g., #ff0000 for red
    color: white;
}
```

### 3. Change Default Values

#### Solver Defaults
**File**: `tabs/solver_tab.py`, Lines 90-95
```python
self.solver_widgets['time_step'] = QDoubleSpinBox(value=0.01)  # Change 0.01
self.solver_widgets['max_steps'] = QSpinBox(value=10)          # Change 10
```

#### Physical Properties
**File**: `tabs/physical_tab.py`, Lines 35-40
```python
add_param("Fluid density:", "rho", 1000, 0, 0)  # Change 1000
```

### 4. Add New Equation Type
**File**: `tabs/solver_tab.py`, Lines 35-40
```python
self.solver_widgets['fluid_eqn'] = self._combo([
    "Incompressible Navier-Stokes", 
    "Compressible NS", 
    "Euler", 
    "Stokes",
    "Your New Equation"  # Add here
])
```

### 5. Change Tab Names
**File**: `main.py`, Lines 78-83
```python
self.tabs.addTab(self.geometry_tab, "New Name")  # Change "New Name"
```

## Color Palette

Current theme uses:
- **Primary Blue**: `#3b82f6`
- **Hover Blue**: `#2563eb`
- **Background**: `#f7f9fc`
- **Border**: `#cbd5e1`
- **Text**: `#222`

### Alternative Color Schemes

**Dark Theme**:
```python
QWidget { background: #1e293b; color: #e2e8f0; }
QPushButton { background-color: #0ea5e9; }
```

**Green Theme**:
```python
QPushButton { background-color: #10b981; }  # Green
QPushButton:hover { background-color: #059669; }
```

**Red Theme**:
```python
QPushButton { background-color: #ef4444; }  # Red
QPushButton:hover { background-color: #dc2626; }
```

## Rebuild After Changes

### Windows
```batch
build_exe.bat
```

### Linux/macOS
```bash
chmod +x build_exe.sh
./build_exe.sh
```

### Manual
```bash
pyinstaller --clean --onefile --windowed --name "SolverGUI" main.py
```

## File Locations

| Item | Location |
|------|----------|
| Main code | `main.py` |
| Windows build script | `build_exe.bat` |
| Linux/Mac build script | `build_exe.sh` |
| Output executable | `dist/SolverGUI.exe` (or `dist/SolverGUI`) |
| Dependencies | `requirements.txt` |

## Common Code Sections

| What to Change | Line Range | Method |
|----------------|------------|---------|
| Window title | ~46 | `__init__()` |
| Colors/Styling | ~54-67 | `__init__()` stylesheet |
| Tab names | ~103-108 | `init_ui()` |
| Geometry settings | ~115-165 | `create_geometry_tab()` |
| Solver defaults | ~225-290 | `create_solver_tab()` |
| Physical defaults | ~310-320 | `create_physical_tab()` |
| Boundary defaults | ~360-380 | `create_boundary_tab()` |
| Button labels | Search for `QPushButton("` | Various methods |

## Testing Workflow

1. Edit `main.py`
2. Run: `python main.py`
3. Test changes
4. If good, rebuild: `build_exe.bat` (or `.sh`)
5. Test `dist/SolverGUI.exe`
6. Share the executable

## Tips

- **Search for text**: Use Ctrl+F to find specific strings to change
- **Backup first**: Copy `main.py` before major changes
- **Test incrementally**: Make one change at a time
- **Check console**: Run from terminal to see error messages
- **Line numbers**: Enable in your editor to find sections quickly

## Getting Help

1. Check `README.md` for detailed guide
2. Look at inline comments in `main.py`
3. Search for examples in the code (most patterns repeat)
4. PySide6 docs: https://doc.qt.io/qtforpython/
