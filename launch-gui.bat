@echo off
echo Website Screenshot Tool Launcher
echo ==============================
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

:: Create virtual environment if it doesn't exist
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    if %ERRORLEVEL% NEQ 0 (
        echo Failed to create virtual environment.
        pause
        exit /b 1
    )
    
    echo Installing dependencies in virtual environment...
    call venv\Scripts\activate
    python -m pip install --upgrade pip
    pip install selenium
    call venv\Scripts\deactivate.bat
) else (
    echo Using existing virtual environment...
)

:: Create screenshots directories if they don't exist
if not exist "screenshots" mkdir screenshots
if not exist "screenshots_full" mkdir screenshots_full

:: Check if the GUI script exists
if not exist "simple_gui.py" (
    echo Error: simple_gui.py not found in the current directory.
    echo Please make sure the file is in the same directory as this batch file.
    pause
    exit /b 1
)

:: Launch the GUI using the virtual environment
echo Launching the GUI with virtual environment...
call venv\Scripts\activate
python simple_gui.py
call venv\Scripts\deactivate.bat

echo.
echo GUI closed.
pause
