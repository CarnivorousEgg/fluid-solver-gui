# Contributing Guide

Thank you for considering contributing to the Solver GUI project!

---

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Git installed
- Basic knowledge of Python and Qt/PySide6

### Setup Development Environment

1. **Fork the repository** (when on GitHub)

2. **Clone your fork**:
```bash
git clone https://github.com/your-username/solver-gui.git
cd solver-gui
```

3. **Create virtual environment**:
```powershell
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/macOS
python3 -m venv .venv
source .venv/bin/activate
```

4. **Install dependencies**:
```powershell
pip install -r requirements.txt
```

5. **Test the application**:
```powershell
python main.py
```

---

## Development Workflow

### 1. Create a Branch

```bash
git checkout -b feature/your-feature-name
```

**Branch naming**:
- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation updates
- `refactor/` - Code refactoring

Examples:
- `feature/add-export-to-csv`
- `fix/boundary-label-bug`
- `docs/update-usage-guide`

### 2. Make Changes

Edit code following our [Code Style](#code-style) guidelines.

### 3. Test Changes

```powershell
# Run the application
python main.py

# Test all tabs
# Test file generation
# Test edge cases
```

### 4. Commit Changes

```bash
git add .
git commit -m "Brief description of changes"
```

**Commit message format**:
```
Type: Brief description

Longer explanation if needed.
```

**Types**: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

**Examples**:
```
feat: Add CSV export functionality

Added export_to_csv() method to output tab.
Users can now export boundary conditions to CSV format.
```

```
fix: Correct boundary label numbering

Fixed _refresh_bc_labels() to properly increment labels.
Previously showed B-2, B-2 instead of B-2, B-3.
```

### 5. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub.

---

## Code Style

### Python Style

Follow PEP 8 with these specifics:

**Indentation**: 4 spaces (not tabs)

**Line Length**: 88 characters (Black default)

**Naming**:
```python
# Functions and variables: snake_case
def calculate_total_force():
    total_force = 0
    
# Classes: PascalCase
class SolverGUI:
    pass
    
# Constants: UPPER_CASE
MAX_ITERATIONS = 1000
```

**Docstrings**: All public methods
```python
def create_solver_tab(self):
    """
    Create the Solver configuration tab.
    
    Returns:
        QWidget: Configured solver tab with all simulation parameters.
    """
    # Implementation...
```

**Comments**: Explain why, not what
```python
# Good
# Filter tag 0 to exclude internal boundaries
if bc['tag'] != 0:

# Not ideal
# Check if tag is not zero
if bc['tag'] != 0:
```

### Qt/PySide6 Style

**Widget Creation**:
```python
# Prefer descriptive names
self.coordinate_file_edit = QLineEdit()
# Not: self.edit1, self.le_coord

# Group related widgets in dictionaries
self.solver_widgets = {
    'sim_type': QComboBox(),
    'time_step': QDoubleSpinBox(),
}
```

**Layout Pattern**:
```python
# Create container
tab = QWidget()
layout = QVBoxLayout(tab)

# Create groups
group = QGroupBox("Title")
group_layout = QFormLayout(group)

# Add widgets
group_layout.addRow("Label:", widget)

# Add to parent
layout.addWidget(group)
return tab
```

**Signal Connection**:
```python
# Use lambda for arguments
button.clicked.connect(lambda: self.on_click(arg))

# Direct connection for no arguments
button.clicked.connect(self.on_click)
```

---

## Project Structure

```
solver-gui/
├── main.py              # Entry point
├── trial.py             # Main application (to be modularized)
├── utils/               # Utilities
│   ├── styles.py        # Styling
│   └── helpers.py       # Helper functions
├── tabs/                # Tab modules
│   └── geometry_tab.py  # Example modular tab
├── docs/                # Documentation
└── tests/               # Tests (future)
```

---

## Adding Features

### Add a New Field

1. **Create the widget** (in appropriate tab method):
```python
self.my_field = QLineEdit()
self.my_field.setPlaceholderText("Enter value")
```

2. **Add to layout**:
```python
form_layout.addRow("My Field:", self.my_field)
```

3. **Store value** (if needed):
```python
self.data_dict['my_field'] = self.my_field
```

4. **Use in output** (in `save_input_file()`):
```python
f.write(f"myField = {self.my_field.text()}\n")
```

### Add a New Tab

1. **Create tab method**:
```python
def create_mytab_tab(self):
    """Create My Tab configuration."""
    tab = QWidget()
    layout = QVBoxLayout(tab)
    
    # Add your components...
    
    return tab
```

2. **Add to `init_ui()`**:
```python
self.tabs.addTab(self.create_mytab_tab(), "My Tab")
```

### Add a New Modular Tab

See `tabs/geometry_tab.py` as template:

1. **Create file**: `tabs/mytab_tab.py`

2. **Define class**:
```python
from PySide6.QtWidgets import QWidget, QVBoxLayout
from utils.helpers import create_combo_box

class MyTabTab(QWidget):
    """My Tab configuration tab."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
    
    def init_ui(self):
        """Initialize the UI."""
        layout = QVBoxLayout(self)
        # Add components...
    
    def get_data(self):
        """Return tab data."""
        return {"field": self.field_edit.text()}
```

3. **Import in `main.py`** (when modularization complete):
```python
from tabs.mytab_tab import MyTabTab
```

---

## Testing Guidelines

### Manual Testing Checklist

When making changes, test:

- [ ] Application starts without errors
- [ ] All tabs are visible
- [ ] All fields accept input
- [ ] File browsing works
- [ ] Add/Remove buttons work
- [ ] Save file generates correct output
- [ ] Boundary labels update correctly
- [ ] Dropdown menus have all options
- [ ] Styling looks correct
- [ ] No console errors

### Edge Cases to Test

- Empty fields
- Very large numbers
- Negative numbers (where invalid)
- Long file paths
- Special characters in filenames
- Many boundary conditions (20+)
- Rapid add/remove actions

---

## Documentation

### Update Documentation When:

- Adding new features → Update [USAGE.md](USAGE.md)
- Changing code structure → Update [CODE_STRUCTURE.md](CODE_STRUCTURE.md)
- Finding new issues → Update [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- Changing build process → Update [BUILD.md](BUILD.md)
- Adding dependencies → Update [INSTALLATION.md](INSTALLATION.md)

### Documentation Style

- Use clear headings
- Include code examples
- Add screenshots for UI changes (future)
- Keep examples simple and focused

---

## Pull Request Guidelines

### Before Submitting

- [ ] Code follows style guidelines
- [ ] All existing functionality still works
- [ ] Documentation updated
- [ ] Commit messages are clear
- [ ] No debugging print statements left in code
- [ ] No commented-out code blocks

### PR Description Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Code refactoring

## Testing
Describe testing done

## Checklist
- [ ] Code follows project style
- [ ] Documentation updated
- [ ] All features tested
```

---

## Common Tasks

### Modify Styling

Edit `trial.py` lines 54-67 (or `utils/styles.py` if modularized):

```python
self.setStyleSheet("""
    QPushButton {
        background-color: #NEW_COLOR;
    }
""")
```

### Add Dropdown Option

Find combo box creation:
```python
combo = self._combo(["Option 1", "Option 2"])
```

Add your option:
```python
combo = self._combo(["Option 1", "Option 2", "New Option"])
```

Update mapping in `save_input_file()` if needed:
```python
option_map = {
    "Option 1": "value1",
    "Option 2": "value2",
    "New Option": "newvalue",  # Add this
}
```

### Change Default Values

Find widget creation:
```python
spin_box = QDoubleSpinBox()
spin_box.setValue(1.0)  # Change this default
```

---

## Code Review

### What We Look For

- **Correctness**: Does it work as intended?
- **Style**: Follows project conventions?
- **Clarity**: Is code readable?
- **Documentation**: Changes documented?
- **Testing**: Has it been tested?

### Review Process

1. Maintainer reviews PR
2. Requests changes if needed
3. You make updates
4. Approved and merged

---

## Reporting Issues

### Bug Reports

Include:
- **Description**: What happened?
- **Expected**: What should happen?
- **Steps to reproduce**: How to see the bug?
- **Environment**: Python version, OS, PySide6 version
- **Error message**: Full traceback if available

### Feature Requests

Include:
- **Description**: What feature?
- **Use case**: Why is it needed?
- **Suggestion**: How might it work?

---

## Getting Help

### Questions?

- Check [documentation](../README.md)
- Read [code structure guide](CODE_STRUCTURE.md)
- Look at existing code for examples

### Discussion

- Open an issue for general questions
- Tag with `question` label

---

## Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md (future)
- Credited in release notes
- Appreciated! 🎉

---

## License

By contributing, you agree that your contributions will be licensed under the project's license.

---

Thank you for contributing to Solver GUI! 🚀
