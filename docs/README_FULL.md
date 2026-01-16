# Fluid-Acoustic Solver GUI

> A cross-platform graphical interface for configuring fluid-acoustic solver simulations with moving boundaries.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![PySide6](https://img.shields.io/badge/PySide6-6.6+-green.svg)](https://pypi.org/project/PySide6/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## ✨ Features

- ✅ **Cross-platform**: Works on Windows, Linux, and macOS
- ✅ **User-friendly**: Intuitive tab-based interface
- ✅ **Comprehensive**: Configure geometry, solver, physical properties, boundary conditions, and output
- ✅ **Flexible**: Support for multiple equation types (Navier-Stokes, Euler, Stokes, LPCE, etc.)
- ✅ **Dynamic**: Add/remove boundary conditions and prescribed motions as needed
- ✅ **Standalone**: Can be compiled into a single executable file

---

## Installation

### Prerequisites

- **Python 3.8 or higher**
- **pip** (Python package manager)

### Install Dependencies

```bash
# Windows (PowerShell)
pip install PySide6

# Linux/macOS
pip3 install PySide6
```

### Run the Application

```bash
# Windows
python main.py

# Linux/macOS
python3 main.py
```

---

## Building Executable

Create a standalone executable that can run without Python installed.

### Install PyInstaller

```bash
# Windows
pip install pyinstaller

# Linux/macOS
pip3 install pyinstaller
```

### Build for Your Platform

#### Windows

```batch
# Using the provided batch file (recommended)
build_exe.bat

# Or manually
pyinstaller --onefile --windowed --name "SolverGUI" main.py
```

**Output**: `dist\SolverGUI.exe`

#### Linux

```bash
# Create build script (optional)
chmod +x build_exe.sh

# Build executable
pyinstaller --onefile --windowed --name "SolverGUI" main.py
```

**Output**: `dist/SolverGUI`

#### macOS

```bash
# Build executable
pyinstaller --onefile --windowed --name "SolverGUI" trial.py

# Create .app bundle (optional)
pyinstaller --onefile --windowed --name "SolverGUI" --osx-bundle-identifier com.solver.gui main.py
```

**Output**: `dist/SolverGUI.app` or `dist/SolverGUI`

### Build Options Explained

| Option | Description |
|--------|-------------|
| `--onefile` | Package everything into a single executable |
| `--windowed` | Don't show console window (GUI only) |
| `--name "SolverGUI"` | Name of the output executable |
| `--icon=icon.ico` | Add custom icon (optional) |

### Distribution

The executable in the `dist/` folder is standalone and can be:
- Copied to any compatible computer
- Shared without requiring Python installation
- Run directly without dependencies

---

## Customization Guide

### 🎨 Changing Colors and Appearance

**Method 1: Edit utils/styles.py** (Recommended for modular structure)
```python
COLORS = {
    'background': '#f7f9fc',      # Change this
    'primary': '#3b82f6',         # Change this
    # ... etc
}
```

**Method 2: Edit trial.py directly** (If not using modular structure)

Edit the stylesheet in `trial.py` (lines 54-67):

```python
self.setStyleSheet("""
    QWidget { 
        background: #f7f9fc;      # Background color
        color: #222;               # Text color
        font-family: 'Segoe UI';   # Font family
        font-size: 11pt;           # Font size
    }
    QPushButton { 
        background-color: #3b82f6; # Button color
        color: white;
    }
""")
```

**Color Palette**:
- Background: `#f7f9fc` (light blue-gray)
- Primary Button: `#3b82f6` (blue)
- Hover: `#2563eb` (darker blue)
- Border: `#cbd5e1` (light gray)

### 🔢 Changing Default Values

#### Solver Settings (lines 210-240)

```python
# Example: Change default time step
self.solver_widgets['time_step'] = QDoubleSpinBox(
    value=0.01,      # Default value - CHANGE THIS
    decimals=4,      # Number of decimal places
    maximum=10000    # Maximum allowed value
)
```

#### Physical Properties (lines 290-310)

```python
# Example: Change default fluid density
add_param("Fluid density:", "rho", 1000, 0, 0)
#                                    ^^^^
#                                Default value - CHANGE THIS
```

### 📝 Changing Tab Names

Edit `init_ui()` method (lines 90-100):

```python
self.tabs.addTab(self.create_geometry_tab(), "Geometry")  # Change "Geometry" here
self.tabs.addTab(self.create_solver_tab(), "Solver")      # Change "Solver" here
# etc...
```

### 🔘 Changing Button Labels

Search for `QPushButton("text")` and modify the text:

```python
# Example: Change "Browse" to "Select File"
btn_browse = QPushButton("Select File")  # Was "Browse"
```

### 🪟 Changing Window Size

In `__init__()` method (line 48):

```python
# Current: Opens maximized
self.showMaximized()

# Alternative: Fixed size
self.resize(1400, 900)  # width, height in pixels

# Alternative: Fullscreen
self.showFullScreen()
```

### ➕ Adding New Input Fields

Example: Add a new solver parameter

```python
# 1. Add to solver tab (in create_solver_tab method)
self.solver_widgets['new_param'] = QDoubleSpinBox(value=1.0)
form.addRow("New Parameter:", self.solver_widgets['new_param'])

# 2. Add to output file (in save_input_file method)
f.write(f"newParameter = {self.solver_widgets['new_param'].value()}\n")
```

---

## Usage

### Workflow

1. **Geometry Tab**: Load coordinate and connectivity files, add boundary files
2. **Solver Tab**: Configure simulation type, equations, time integration, and solver parameters
3. **Physical Properties Tab**: Set fluid parameters (density, viscosity, speed of sound, etc.)
4. **Boundary Conditions Tab**: Define initial conditions and boundary conditions for each variable
5. **Prescribed Conditions Tab**: Configure prescribed motions (heave, pitch, morph)
6. **Output Data Tab**: Specify probe locations and surface output files
7. **Generate**: Click "Complete the pre-processing" to save the input file

### Output File Format

The application generates a text file with all configuration parameters in the format:

```
// Input file for solver

// Geometry details
crdFile = problem.crd
cnnFile = problem.fluid.cnn
elemType = 4NodeQuad

// Solver details
solverType = transient
fluidEqn = navierStokes
...
```

---

## File Structure

```
solver-gui/
├── main.py                  # Application entry point ⭐ RUN THIS
├── trial.py                 # Complete application code (monolithic)
├── trial_backup.py          # Backup of original code
│
├── tabs/                    # Tab modules (modular structure)
│   ├── __init__.py
│   ├── geometry_tab.py      # Geometry configuration
│   ├── solver_tab.py        # Solver settings (stub)
│   ├── physical_tab.py      # Physical properties (stub)
│   ├── boundary_tab.py      # Boundary conditions (stub)
│   ├── prescribed_tab.py    # Prescribed motions (stub)
│   └── output_tab.py        # Output configuration (stub)
│
├── utils/                   # Utility modules
│   ├── __init__.py
│   ├── styles.py            # Application styling
│   └── helpers.py           # Helper functions
│
├── build_exe.bat            # Windows build script
├── build_exe.sh             # Linux/macOS build script
├── requirements.txt         # Python dependencies
├── README.md                # This file
├── CUSTOMIZATION.md         # Quick customization guide
├── MODULARIZATION_GUIDE.md  # Guide for completing modularization
└── .gitignore               # Git ignore rules
```

---

## Code Structure

### Main Components

| Component | Purpose |
|-----------|---------|
| `SolverGUI.__init__()` | Initialize window, styling, and data storage |
| `init_ui()` | Create main layout and tabs |
| `create_geometry_tab()` | Build geometry configuration interface |
| `create_solver_tab()` | Build solver settings interface |
| `create_physical_tab()` | Build physical properties interface |
| `create_boundary_tab()` | Build boundary conditions interface |
| `create_prescribed_tab()` | Build prescribed motions interface |
| `create_output_tab()` | Build output configuration interface |
| `save_input_file()` | Generate output configuration file |

### Helper Methods

| Method | Purpose |
|--------|---------|
| `add_geometry_row()` | Add boundary file row in geometry tab |
| `add_bc_row()` | Add boundary condition row |
| `add_prescribed_tag()` | Add prescribed motion condition group |
| `_refresh_geom_ui()` | Renumber geometry boundary labels |
| `_refresh_bc_labels()` | Renumber boundary condition labels |
| `_browse_file()` | Open file browser dialog |

---

## Troubleshooting

### Application Won't Start

**Issue**: Python not found or dependencies missing

**Solution**:
```bash
# Check Python version
python --version  # Should be 3.8+

# Reinstall dependencies
pip install --upgrade PySide6
```

### Build Fails

**Issue**: PyInstaller errors during build

**Solution**:
```bash
# Clean previous builds
rmdir /s build dist  # Windows
rm -rf build dist    # Linux/macOS

# Rebuild
pip install --upgrade pyinstaller
pyinstaller --clean --onefile --windowed --name "SolverGUI" trial.py
```

### Executable Too Large

**Issue**: .exe file is 100+ MB

**Solution**: This is normal for PySide6 applications. To reduce size:
```bash
# Use UPX compression (optional)
pip install pyinstaller[upx]
pyinstaller --onefile --windowed --name "SolverGUI" --upx-dir=/path/to/upx trial.py
```

### GUI Looks Different on Linux/macOS

**Issue**: Fonts or colors don't match Windows

**Solution**: Update the stylesheet font-family in `trial.py`:
```python
# For cross-platform compatibility
font-family: Arial, sans-serif;  # Instead of 'Segoe UI'
```

### Output File Not Generated

**Issue**: Nothing happens when clicking "Complete the pre-processing"

**Solution**: Check console for errors. Ensure you have write permissions in the selected directory.

---

## Development Tips

### Testing Changes

1. Edit `trial.py`
2. Run directly: `python trial.py`
3. Test functionality
4. If satisfied, rebuild: `build_exe.bat`

### Version Control

Add to `.gitignore`:
```
build/
dist/
*.spec
__pycache__/
*.pyc
```

### Adding Dependencies

1. Update `requirements.txt`:
```
PySide6==6.6.0
pyinstaller==6.16.0
```

2. Install: `pip install -r requirements.txt`

### Code Formatting

For better readability:
- Use 4 spaces for indentation
- Keep lines under 100 characters
- Add comments before complex sections
- Use descriptive variable names

---

## License

This project is open-source. Feel free to modify and distribute.

---

## Support

For issues or questions:
1. Check the [Troubleshooting](#troubleshooting) section
2. Review inline code comments in `trial.py`
3. Consult PySide6 documentation: https://doc.qt.io/qtforpython/

---

## Version History

### v1.0.0 (Current)
- Initial release
- Support for all major solver equations
- Cross-platform compatibility
- Comprehensive boundary condition support
- Acoustic NRBC parameters
- Prescribed motion configurations

---

**Happy Solving! 🚀**

---

## 📦 For GitHub

### First-Time Setup

```bash
git init
git add .
git commit -m "Initial commit: Fluid-Acoustic Solver GUI"
git branch -M main
git remote add origin https://github.com/yourusername/solver-gui.git
git push -u origin main
```

### Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Test thoroughly (`python main.py`)
5. Commit (`git commit -m 'Add amazing feature'`)
6. Push (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Recommended .gitignore

Already included in the project. Key exclusions:
- `__pycache__/`, `*.pyc` - Python bytecode
- `dist/`, `build/`, `*.spec` - Build artifacts  
- `.venv/`, `venv/` - Virtual environments
- `*.zip` - Distribution packages

---

## 📄 License

This project is open-source and available under the MIT License.

---

## 🤝 Support

- **Issues**: Open an issue on GitHub
- **Discussions**: Use GitHub Discussions for questions
- **Documentation**: Check `CUSTOMIZATION.md` for quick ref
- **Modularization**: See `MODULARIZATION_GUIDE.md` for refactoring

---

## 🎯 Roadmap

- [x] Basic GUI with all tabs
- [x] File export functionality
- [x] Cross-platform compatibility
- [x] Modular structure setup
- [ ] Complete tab modularization
- [ ] Unit tests
- [ ] CI/CD pipeline
- [ ] Plugin system
- [ ] Configuration presets

---

**Made with ❤️ for computational fluid dynamics**
