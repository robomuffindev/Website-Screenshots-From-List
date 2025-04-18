@echo off
echo Website Screenshot Tool - Complete Setup
echo ======================================
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

:: Install pre-compiled Pillow wheel instead of building from source
echo Installing Pillow (pre-compiled)...
pip install --only-binary :all: pillow

:: Create necessary directories if they don't exist
echo Creating directory structure...
if not exist "screenshots" mkdir screenshots
if not exist "screenshots_full" mkdir screenshots_full
if not exist "drivers" mkdir drivers

:: Check for example URLs file
if not exist "urls.txt" (
    echo Creating example URLs file...
    echo google.com> urls.txt
    echo github.com>> urls.txt
    echo example.com>> urls.txt
    echo wikipedia.org>> urls.txt
    echo microsoft.com>> urls.txt
)

echo.
echo Setup completed successfully!
echo.
echo You can now use:
echo - launch-gui.bat   For the graphical interface
echo - run.bat          For regular screenshots (1920x1920)
echo - run-full.bat     For full-page screenshots (1920xHeight)
echo.
echo See README.md for more information.
echo.

pause