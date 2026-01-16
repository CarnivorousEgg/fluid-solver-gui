@echo off
echo Building Solver GUI executable...
pyinstaller --onefile --windowed --name "SolverGUI" main.py
echo.
echo Build complete! Executable is in the 'dist' folder
pause
