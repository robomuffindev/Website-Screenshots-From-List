@echo off
echo Setting up Website Screenshot GUI Tool...
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
)

:: Activate virtual environment and install dependencies
echo Installing dependencies...
call venv\Scripts\activate
python -m pip install --upgrade pip
pip install selenium==4.11.2

echo.
echo Setup completed successfully!
echo.
echo To run the GUI tool, use run-gui.bat
echo.

pause