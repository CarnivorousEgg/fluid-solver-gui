# Fluid-Acoustic Solver GUI

A Python-based graphical interface for configuring fluid and acoustic simulation parameters.

---

## Quick Start

### Prerequisites
- Python 3.8 or higher
- Windows/Linux/macOS

### Installation

1. **Clone/Download** this repository

2. **Install dependencies**:
```powershell
pip install -r requirements.txt
```

3. **Run the application**:
```powershell
python main.py
```

### Building Executable

**Windows**:
```powershell
build_exe.bat
```

**Linux/macOS**:
```bash
chmod +x build_exe.sh
./build_exe.sh
```

Executable will be in `dist/` folder.

---

## Documentation Index

Complete documentation is organized in the `docs/` folder:

| Document | Description |
|----------|-------------|
| [Installation Guide](docs/INSTALLATION.md) | Platform-specific installation instructions |
| [Usage Guide](docs/USAGE.md) | How to use each tab and generate output files |
| [Build Guide](docs/BUILD.md) | Creating executables with PyInstaller |
| [Customization](docs/CUSTOMIZATION.md) | Quick customization reference |
| [Code Structure](docs/CODE_STRUCTURE.md) | Codebase architecture and organization |
| [Troubleshooting](docs/TROUBLESHOOTING.md) | Common issues and solutions |
| [Contributing](docs/CONTRIBUTING.md) | How to contribute to the project |

---

## Features

- **6 Configuration Tabs**: Geometry, Solver, Physical Properties, Boundary Conditions, Prescribed Conditions, Output Data
- **Fluid Equations**: Incompressible/Compressible Navier-Stokes, Stokes, Euler
- **Acoustic Support**: LPCE equation with NRBC parameters, acoustic potential boundary conditions
- **Structural Analysis**: Displacement fields with material properties
- **Dynamic UI**: Add/remove boundary conditions, prescribed conditions, and output fields
- **File Generation**: Creates formatted input files for simulation software

---

## Basic Workflow

1. **Geometry Tab**: Specify mesh files (coordinates, connectivity, boundaries)
2. **Solver Tab**: Choose equation type, set time stepping and convergence parameters
3. **Physical Properties Tab**: Define material properties (density, viscosity, etc.)
4. **Boundary Conditions Tab**: Assign boundary types and values
5. **Prescribed Conditions Tab**: Set time-varying conditions (optional)
6. **Output Tab**: Select fields to output
7. **Save**: Click "Save Input File" button

---

## Screenshots

*(Coming soon)*

---

## Requirements

- **Python**: 3.8+
- **PySide6**: 6.6.0+ (Qt for Python)
- **PyInstaller**: 6.0.0+ (for building executables)

See [requirements.txt](requirements.txt) for full list.

---

## Project Structure

```
solver-gui/
├── main.py                  # Entry point
├── trial.py                 # Main application
├── utils/                   # Utilities (styling, helpers)
├── tabs/                    # Tab modules (modular structure)
├── docs/                    # Documentation
├── build_exe.bat            # Windows build script
├── build_exe.sh             # Linux/macOS build script
└── requirements.txt         # Dependencies
```

---

## License

*(Add license information here)*

---

## Support

For issues, questions, or contributions:
- See [Troubleshooting Guide](docs/TROUBLESHOOTING.md)
- See [Contributing Guide](docs/CONTRIBUTING.md)
- Open an issue on GitHub

---

## Acknowledgments

Developed for fluid-acoustic coupled simulations with support for structural analysis.

---

**Quick Links**:
- 📦 [Installation](docs/INSTALLATION.md)
- 📖 [Usage Guide](docs/USAGE.md)
- 🔧 [Customization](docs/CUSTOMIZATION.md)
- ❓ [Troubleshooting](docs/TROUBLESHOOTING.md)
