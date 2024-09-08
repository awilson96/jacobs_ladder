@echo off
echo Starting WinAppDriver...
"C:\Program Files (x86)\Windows Application Driver\WinAppDriver.exe"

echo WinAppDriver is running. Press Ctrl+C to stop.
:loop
timeout /t 5 /nobreak >nul
goto loop
