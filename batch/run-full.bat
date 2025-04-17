@echo off
setlocal EnableDelayedExpansion
echo Website Full-Page Screenshot Tool
echo.

:: Check if the virtual environment exists
if not exist "venv" (
    echo Virtual environment not found. Please run setup.bat first.
    pause
    exit /b 1
)

:: If no file was provided as an argument, check if urls.txt exists
if "%~1"=="" (
    if exist "urls.txt" (
        echo Using default file: urls.txt
        set "url_file=urls.txt"
    ) else (
        echo No URL file provided and urls.txt not found.
        echo.
        set /p url_file="Enter the name of your URL file: "
        
        if "!url_file!"=="" (
            echo No file specified. Exiting.
            pause
            exit /b 1
        )
    )
) else (
    set "url_file=%~1"
)

:: Check if the URL file exists
if not exist "!url_file!" (
    echo File not found: !url_file!
    pause
    exit /b 1
)

echo Using URL file: !url_file!
echo.

:: Activate the virtual environment and run the script with increased timeout
call venv\Scripts\activate
set PYTHONIOENCODING=utf-8
python website_screenshot_full.py "!url_file!"

:: Deactivate the virtual environment
call venv\Scripts\deactivate.bat
endlocal