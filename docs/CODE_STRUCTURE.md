# Code Structure

## Overview

The application is organized into modular components for easy maintenance.

---

## File Organization

```
solver-gui/
│
├── main.py                  # Entry point
├── trial.py                 # Complete application (monolithic)
├── trial_backup.py          # Original backup
│
├── tabs/                    # Tab modules (modular)
│   ├── geometry_tab.py      # Geometry configuration
│   └── __init__.py
│
├── utils/                   # Shared utilities
│   ├── styles.py            # Application styling  
│   ├── helpers.py           # Helper functions
│   └── __init__.py
│
├── docs/                    # Documentation
└── build scripts, etc.
```

---

## Main Components

### main.py
**Purpose**: Application entry point

```python
from trial import SolverGUI  # Import main class
app = QApplication(sys.argv)
window = SolverGUI()
window.show()
```

**Customization**: Change window, tabs, or imports here

---

### trial.py
**Purpose**: Complete application code

**Structure**:
```python
class SolverGUI(QWidget):
    def __init__():           # Initialize window, styling
    def init_ui():            # Create tabs and layout
    
    # Tab creation methods
    def create_geometry_tab()
    def create_solver_tab()
    def create_physical_tab()
    def create_boundary_tab()
    def create_prescribed_tab()
    def create_output_tab()
    
    # Helper methods
    def add_geometry_row()
    def add_bc_row()
    def calculate_nondim()
    
    # File generation
    def save_input_file()
```

**Key Sections**:
- Lines 1-40: Imports and documentation
- Lines 40-80: Styling (`setStyleSheet`)
- Lines 80-120: Init and data storage
- Lines 120-240: Geometry tab
- Lines 240-390: Solver tab
- Lines 390-475: Physical properties tab
- Lines 475-650: Boundary conditions tab
- Lines 650-720: Prescribed conditions tab
- Lines 720-795: Output data tab
- Lines 795-1000: File generation logic

---

## Modular Structure (In Progress)

### utils/styles.py
**Purpose**: Centralized styling

**Contents**:
```python
COLORS = {                    # Color palette
    'background': '#f7f9fc',
    'primary': '#3b82f6',
    ...
}

APP_STYLESHEET = """..."""    # Complete CSS

def get_stylesheet():         # Returns stylesheet
```

**Customization**: Edit `COLORS` dictionary

---

### utils/helpers.py
**Purpose**: Shared utility functions

**Functions**:
```python
create_combo_box(items)       # Create dropdown
browse_file(parent, edit)     # File browser dialog
save_file_dialog(parent)      # Save dialog
```

**Usage**: Import and use in tabs

---

### tabs/geometry_tab.py
**Purpose**: Geometry configuration tab (example modular tab)

**Class**: `GeometryTab(QWidget)`

**Methods**:
```python
__init__(parent)              # Initialize
init_ui()                     # Create UI
create_mesh_config()          # Mesh section
create_boundary_files()       # Boundary section
add_boundary_row()            # Add row
remove_boundary_row()         # Remove row
get_boundary_rows()           # Get data
```

**Pattern**: Other tabs should follow this structure

---

## Data Flow

### Input Flow
```
User Input (GUI)
    ↓
Widget Values (QLineEdit, QSpinBox, etc.)
    ↓
Collection (in save_input_file())
    ↓
Formatting (text generation)
    ↓
Output File (inputFile.txt)
```

### Widget Storage
```python
self.coord_edit                    # QLineEdit for coordinate file
self.solver_widgets['sim_type']   # Dictionary of solver widgets  
self.phys_inputs['rho']            # Dictionary of physical inputs
self.init_cond_widgets['pres']     # Dictionary of initial conditions
self.geometry_boundary_rows[]      # List of boundary row dictionaries
```

---

## Key Methods

### Tab Creation Pattern
```python
def create_X_tab(self):
    """Create X configuration tab."""
    tab = QWidget()
    layout = QVBoxLayout(tab)
    
    # Create groups
    group = QGroupBox("Title")
    group_layout = QFormLayout(group)
    
    # Add widgets
    self.widget = QLineEdit()
    group_layout.addRow("Label:", self.widget)
    
    layout.addWidget(group)
    return tab
```

### Dynamic Row Pattern
```python
def add_row(self):
    """Add a new row."""
    row_widget = QWidget()
    row_layout = QHBoxLayout(row_widget)
    
    # Add widgets to row
    label = QLabel(f"Row-{n}")
    edit = QLineEdit()
    btn = QPushButton("Remove")
    
    row_layout.addWidget(label)
    row_layout.addWidget(edit)
    row_layout.addWidget(btn)
    
    # Store row data
    self.rows.append({"widget": row_widget, "edit": edit})
    
    # Add to layout
    self.container_layout.addWidget(row_widget)
```

---

## Widget Types Used

| Widget | Purpose | Example |
|--------|---------|---------|
| `QLineEdit` | Text input | File paths, boundary names |
| `QSpinBox` | Integer input | Iterations, steps |
| `QDoubleSpinBox` | Decimal input | Time step, tolerance |
| `QComboBox` | Dropdown | Equation types, file types |
| `QPushButton` | Buttons | Browse, Add, Remove |
| `QCheckBox` | Toggle | Restart flag |
| `QLabel` | Text display | Field labels, row numbers |
| `QGroupBox` | Section container | Groups of related fields |
| `QTabWidget` | Tabs | Main tabs, BC sub-tabs |
| `QScrollArea` | Scrollable area | Long lists (boundaries, etc.) |

---

## Styling System

### CSS-like Styling
```python
self.setStyleSheet("""
    QPushButton { 
        background-color: #3b82f6;
        color: white;
    }
    QPushButton:hover {
        background-color: #2563eb;
    }
""")
```

### Properties
```python
button.setProperty("secondary", True)  # Adds property
# Styled with: QPushButton[secondary='true'] { ... }
```

---

## File Generation

### Output File Structure
```python
def save_input_file(self):
    # 1. Open save dialog
    path = QFileDialog.getSaveFileName(...)
    
    # 2. Open file
    with open(path, 'w') as f:
        # 3. Write sections
        f.write("// Geometry details\n")
        f.write(f"crdFile = {self.coord_edit.text()}\n")
        
        # 4. Loop through boundary conditions
        for bc in boundary_conditions:
            f.write(f"index = {i}\n")
            f.write(f"type = {bc['type']}\n")
            ...
```

**Key Maps**:
```python
elem_map = {
    "4-Node Quadrilateral": "4NodeQuad",
    "3-Node Triangle": "3NodeTri",
    ...
}

fluid_eqn_map = {
    "Incompressible Navier-Stokes": "navierStokes",
    ...
}
```

---

## Adding Features

### Add New Tab
1. Create method: `def create_mytab_tab(self):`
2. Add to `init_ui()`: `self.tabs.addTab(self.create_mytab_tab(), "My Tab")`
3. Follow existing tab pattern

### Add New Field
1. Create widget: `self.my_field = QLineEdit()`
2. Add to layout: `form.addRow("My Field:", self.my_field)`
3. Use in `save_input_file()`: `f.write(f"myField = {self.my_field.text()}\n")`

### Add New Dropdown Option
1. Find combo creation: `self._combo([...])`
2. Add to list: `self._combo(["Option 1", "Option 2", "New Option"])`
3. Add mapping in `save_input_file()` if needed

---

## Code Style

### Conventions
- **Indentation**: 4 spaces
- **Naming**: snake_case for methods, variables
- **Docstrings**: All methods have docstrings
- **Comments**: Explain complex logic

### Example
```python
def create_solver_tab(self):
    """
    Create the Solver configuration tab.
    
    Returns:
        QWidget: Configured solver tab
    """
    tab = QWidget()  # Main container
    layout = QVBoxLayout(tab)  # Vertical layout
    
    # Add components...
    
    return tab
```

---

## Testing Changes

1. Edit `trial.py`
2. Run: `python main.py`
3. Test functionality
4. If good, rebuild: `build_exe.bat`

---

## Next Steps

- [Customization Guide](CUSTOMIZATION.md) - Make changes
- [Usage Guide](USAGE.md) - Understand features
