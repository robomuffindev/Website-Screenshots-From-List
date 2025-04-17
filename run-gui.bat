@echo off 
setlocal EnableDelayedExpansion 
echo Website Screenshot GUI Tool 
echo. 
 
:: Check if the virtual environment exists 
if not exist "venv" ( 
    echo Virtual environment not found. Please run setup.bat first. 
    pause 
    exit /b 1 
) 
 
:: Activate the virtual environment and run the GUI script 
call venv\Scripts\activate 
set PYTHONIOENCODING=utf-8 
python scripts\website_screenshot_gui.py 
 
:: Deactivate the virtual environment 
call venv\Scripts\deactivate.bat 
endlocal 
