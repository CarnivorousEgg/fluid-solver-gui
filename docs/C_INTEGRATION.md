# Integrating C Pre/Post Processing Programs

This guide explains how to add C programs for preprocessing and postprocessing into the GUI application.

---

## Overview

You can integrate C programs that handle:
- **Preprocessing**: Process input files before simulation
- **Postprocessing**: Analyze output files after simulation

There are three main approaches, from simplest to most complex.

---

## Option 1: Call C Executables (Recommended)

**Best for**: Existing compiled C programs that you want to call from the GUI.

### Step 1: Prepare Your C Programs

Compile your C code into executables:

```bash
# Windows
gcc preprocessor.c -o preprocessor.exe
gcc postprocessor.c -o postprocessor.exe

# Linux/macOS
gcc preprocessor.c -o preprocessor
gcc postprocessor.c -o postprocessor
```

Place the executables in your project root or a `bin/` folder.

### Step 2: Add Buttons to GUI

Edit `tabs/output_tab.py` to add preprocessing/postprocessing buttons:

```python
# In tabs/output_tab.py, modify init_ui method

def init_ui(self):
    """Initialize the output tab UI."""
    layout = QVBoxLayout(self)
    
    # ... existing probe and surface groups ...
    
    # Add Processing Tools section
    processing_group = QGroupBox("Processing Tools")
    processing_layout = QVBoxLayout(processing_group)
    
    # Preprocessing button
    btn_preprocess = QPushButton("Run C Preprocessor")
    btn_preprocess.setProperty("secondary", True)
    btn_preprocess.clicked.connect(self.run_preprocessor)
    processing_layout.addWidget(btn_preprocess)
    
    # Postprocessing button
    btn_postprocess = QPushButton("Run C Postprocessor")
    btn_postprocess.setProperty("secondary", True)
    btn_postprocess.clicked.connect(self.run_postprocessor)
    processing_layout.addWidget(btn_postprocess)
    
    # Status label
    self.processing_status = QLabel("")
    processing_layout.addWidget(self.processing_status)
    
    layout.addWidget(processing_group)
    
    # ... rest of existing code ...
```

### Step 3: Implement Runner Methods

Add these methods to the `OutputTab` class:

```python
import subprocess
import os
from PySide6.QtWidgets import QMessageBox

def run_preprocessor(self):
    """Run the C preprocessor executable."""
    try:
        self.processing_status.setText("Running preprocessor...")
        self.processing_status.setStyleSheet("color: #3b82f6;")
        
        # Path to your C executable
        exe_path = "./bin/preprocessor.exe"  # Adjust path as needed
        
        # Check if file exists
        if not os.path.exists(exe_path):
            raise FileNotFoundError(f"Preprocessor not found: {exe_path}")
        
        # Run the C program
        result = subprocess.run(
            [exe_path, "inputFile.txt"],  # Pass input file as argument
            capture_output=True,
            text=True,
            timeout=60  # 60 second timeout
        )
        
        # Check result
        if result.returncode == 0:
            self.processing_status.setText(f"✓ Preprocessor completed successfully")
            self.processing_status.setStyleSheet("color: #10b981;")
            print(result.stdout)  # Print output to console
        else:
            self.processing_status.setText(f"✗ Preprocessor failed")
            self.processing_status.setStyleSheet("color: #ef4444;")
            print(result.stderr)  # Print errors
            
    except subprocess.TimeoutExpired:
        self.processing_status.setText("✗ Preprocessor timed out")
        self.processing_status.setStyleSheet("color: #ef4444;")
        QMessageBox.warning(self, "Timeout", "Preprocessor took too long to complete")
        
    except FileNotFoundError as e:
        self.processing_status.setText("✗ Preprocessor not found")
        self.processing_status.setStyleSheet("color: #ef4444;")
        QMessageBox.critical(self, "Error", str(e))
        
    except Exception as e:
        self.processing_status.setText(f"✗ Error: {str(e)}")
        self.processing_status.setStyleSheet("color: #ef4444;")
        print(f"Error running preprocessor: {e}")

def run_postprocessor(self):
    """Run the C postprocessor executable."""
    try:
        self.processing_status.setText("Running postprocessor...")
        self.processing_status.setStyleSheet("color: #3b82f6;")
        
        # Path to your C executable
        exe_path = "./bin/postprocessor.exe"  # Adjust path as needed
        
        # Check if file exists
        if not os.path.exists(exe_path):
            raise FileNotFoundError(f"Postprocessor not found: {exe_path}")
        
        # Run the C program with output files
        result = subprocess.run(
            [exe_path, "outputFile.vtk"],  # Pass output file as argument
            capture_output=True,
            text=True,
            timeout=120  # 2 minute timeout
        )
        
        # Check result
        if result.returncode == 0:
            self.processing_status.setText(f"✓ Postprocessor completed successfully")
            self.processing_status.setStyleSheet("color: #10b981;")
            print(result.stdout)
        else:
            self.processing_status.setText(f"✗ Postprocessor failed")
            self.processing_status.setStyleSheet("color: #ef4444;")
            print(result.stderr)
            
    except subprocess.TimeoutExpired:
        self.processing_status.setText("✗ Postprocessor timed out")
        self.processing_status.setStyleSheet("color: #ef4444;")
        QMessageBox.warning(self, "Timeout", "Postprocessor took too long to complete")
        
    except FileNotFoundError as e:
        self.processing_status.setText("✗ Postprocessor not found")
        self.processing_status.setStyleSheet("color: #ef4444;")
        QMessageBox.critical(self, "Error", str(e))
        
    except Exception as e:
        self.processing_status.setText(f"✗ Error: {str(e)}")
        self.processing_status.setStyleSheet("color: #ef4444;")
        print(f"Error running postprocessor: {e}")
```

### Step 4: Include in Executable Build

To bundle C executables with your PyInstaller build, edit `build_exe.bat`:

```batch
pyinstaller ^
    --onefile ^
    --windowed ^
    --name "FluidAcousticSolver" ^
    --add-binary "bin/preprocessor.exe;bin" ^
    --add-binary "bin/postprocessor.exe;bin" ^
    main.py
```

Or for Linux/macOS in `build_exe.sh`:

```bash
pyinstaller \
    --onefile \
    --windowed \
    --name "FluidAcousticSolver" \
    --add-binary "bin/preprocessor:bin" \
    --add-binary "bin/postprocessor:bin" \
    main.py
```

---

## Option 2: Use ctypes (For C Libraries)

**Best for**: When you want to call C functions directly from Python without creating separate executables.

### Step 1: Compile as Shared Library

```bash
# Windows (creates .dll)
gcc -shared -o myprocessor.dll -fPIC preprocessor.c

# Linux (creates .so)
gcc -shared -o myprocessor.so -fPIC preprocessor.c

# macOS (creates .dylib)
gcc -shared -o myprocessor.dylib -fPIC preprocessor.c
```

### Step 2: Load and Call C Functions

```python
import ctypes
import sys

# Load the C library
if sys.platform == 'win32':
    lib = ctypes.CDLL('./myprocessor.dll')
elif sys.platform == 'darwin':
    lib = ctypes.CDLL('./myprocessor.dylib')
else:
    lib = ctypes.CDLL('./myprocessor.so')

# Define function signatures
# Example: int process_file(char* filename)
lib.process_file.argtypes = [ctypes.c_char_p]
lib.process_file.restype = ctypes.c_int

# Call the function
result = lib.process_file(b"inputFile.txt")
if result == 0:
    print("Processing successful")
else:
    print(f"Processing failed with code {result}")
```

### Step 3: Integrate into GUI

```python
def run_preprocessor(self):
    """Run C preprocessing using ctypes."""
    try:
        import ctypes
        import sys
        
        # Load library
        if sys.platform == 'win32':
            lib = ctypes.CDLL('./bin/myprocessor.dll')
        else:
            lib = ctypes.CDLL('./bin/myprocessor.so')
        
        # Set up function
        lib.preprocess.argtypes = [ctypes.c_char_p]
        lib.preprocess.restype = ctypes.c_int
        
        # Call function
        result = lib.preprocess(b"inputFile.txt")
        
        if result == 0:
            self.processing_status.setText("✓ Preprocessing complete")
        else:
            self.processing_status.setText(f"✗ Processing failed: {result}")
            
    except Exception as e:
        print(f"Error: {e}")
        self.processing_status.setText(f"✗ Error: {str(e)}")
```

---

## Option 3: Python Extension Module (Advanced)

**Best for**: Maximum performance and tight integration.

### Create Python Extension

Use Python's C API to create a module:

```c
// preprocessor_module.c
#include <Python.h>

static PyObject* preprocess(PyObject* self, PyObject* args) {
    const char* filename;
    
    if (!PyArg_ParseTuple(args, "s", &filename)) {
        return NULL;
    }
    
    // Your preprocessing code here
    printf("Processing %s\n", filename);
    
    Py_RETURN_NONE;
}

static PyMethodDef Methods[] = {
    {"preprocess", preprocess, METH_VARARGS, "Run preprocessing"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef module = {
    PyModuleDef_HEAD_INIT,
    "preprocessor",
    NULL,
    -1,
    Methods
};

PyMODINIT_FUNC PyInit_preprocessor(void) {
    return PyModule_Create(&module);
}
```

### Build with setuptools

```python
# setup.py
from setuptools import setup, Extension

module = Extension('preprocessor', sources=['preprocessor_module.c'])

setup(
    name='preprocessor',
    version='1.0',
    ext_modules=[module]
)
```

Build: `python setup.py build_ext --inplace`

### Use in Python

```python
import preprocessor
preprocessor.preprocess("inputFile.txt")
```

---

## File Organization

Recommended project structure:

```
solver-gui/
├── main.py
├── tabs/
├── utils/
├── bin/                     # C executables
│   ├── preprocessor.exe
│   └── postprocessor.exe
├── lib/                     # C libraries (optional)
│   ├── myprocessor.dll
│   └── myprocessor.so
└── src/                     # C source code (optional)
    ├── preprocessor.c
    └── postprocessor.c
```

---

## Example C Program

Simple preprocessor that reads input file and validates format:

```c
// preprocessor.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char *argv[]) {
    if (argc < 2) {
        fprintf(stderr, "Usage: %s <inputfile>\n", argv[0]);
        return 1;
    }
    
    FILE *fp = fopen(argv[1], "r");
    if (!fp) {
        fprintf(stderr, "Error: Cannot open file %s\n", argv[1]);
        return 1;
    }
    
    printf("Preprocessing %s...\n", argv[1]);
    
    // Your preprocessing logic here
    char line[1024];
    int line_count = 0;
    while (fgets(line, sizeof(line), fp)) {
        line_count++;
        // Process each line
    }
    
    fclose(fp);
    
    printf("Processed %d lines successfully\n", line_count);
    return 0;
}
```

Compile: `gcc preprocessor.c -o preprocessor.exe`

---

## Testing

1. **Test C program standalone**:
   ```bash
   ./preprocessor.exe inputFile.txt
   ```

2. **Test from Python**:
   ```python
   import subprocess
   result = subprocess.run(["./preprocessor.exe", "inputFile.txt"])
   print(f"Exit code: {result.returncode}")
   ```

3. **Test in GUI**: Click the button and verify status messages

---

## Troubleshooting

### C Executable Not Found
- Check file path is correct
- Verify executable has proper permissions (Linux/macOS: `chmod +x preprocessor`)
- Use absolute paths if relative paths don't work

### Runtime Errors
- Check C program exit codes (0 = success)
- Capture stderr: `subprocess.run(..., capture_output=True)`
- Add timeout to prevent hanging: `timeout=60`

### Build Issues
- Ensure C executables are in `bin/` before building
- Check `--add-binary` paths in PyInstaller command
- Test executable location in dist folder after build

---

## Best Practices

1. **Error Handling**: Always check return codes and handle exceptions
2. **Timeouts**: Set reasonable timeouts to prevent GUI freezing
3. **User Feedback**: Show status messages and progress
4. **Logging**: Print stdout/stderr for debugging
5. **Validation**: Check file existence before calling C programs
6. **Cross-platform**: Test on Windows/Linux/macOS if needed

---

## Summary

**Quickest Solution**: Use **Option 1** (subprocess) - simple, reliable, works with existing C code.

**For Production**: Consider **Option 2** (ctypes) for better integration and performance.

**For Complex Projects**: Use **Option 3** (Python extensions) for maximum performance.

Start with Option 1, then optimize later if needed!
