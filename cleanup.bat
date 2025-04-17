@echo off 
echo Cleaning up screenshot directories... 
echo. 
echo Regular Screenshots: 
for /d %%i in (screenshots\*) do ( 
    echo Found: %%i 
    choice /c YN /m "Delete %%i?" 
    if errorlevel 1 if not errorlevel 2 rmdir /s /q "%%i" 
) 
echo. 
echo Full-Page Screenshots: 
for /d %%i in (screenshots_full\*) do ( 
    echo Found: %%i 
    choice /c YN /m "Delete %%i?" 
    if errorlevel 1 if not errorlevel 2 rmdir /s /q "%%i" 
) 
echo. 
echo Done! 
pause 
