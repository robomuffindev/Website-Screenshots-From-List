@echo off
echo Image Processing Tool
echo ====================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Python is not installed or not in PATH.
    echo Please install Python from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation.
    pause
    exit /b 1
)

:: Activate virtual environment if it exists
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate
    echo Using virtual environment.
) else (
    echo No virtual environment found. Using system Python.
)

:: Check if process_last_screenshots.py exists
if not exist "process_last_screenshots.py" (
    echo Error: process_last_screenshots.py not found in the current directory.
    pause
    exit /b 1
)

:: Run the image processing script
python process_last_screenshots.py %*

:: Deactivate virtual environment if it was activated
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\deactivate.bat
)

echo.
echo Processing complete.
pause
