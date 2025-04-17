@echo off
echo Website Screenshot Tool
echo.

:: Check if the virtual environment exists
if not exist "venv" (
    echo Virtual environment not found. Please run setup.bat first.
    pause
    exit /b 1
)

:: Check if a URL file was provided
if "%~1"=="" (
    echo Usage: run.bat urls.txt
    echo.
    echo Please provide a text file containing URLs (one per line)
    pause
    exit /b 1
)

:: Check if the URL file exists
if not exist "%~1" (
    echo File not found: %~1
    pause
    exit /b 1
)

:: Activate the virtual environment and run the script
call venv\Scripts\activate
python website_screenshot.py "%~1"

:: Deactivate the virtual environment
call venv\Scripts\deactivate.bat