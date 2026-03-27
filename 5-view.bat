@echo off
chcp 65001 >nul
echo ========================================
echo   View Detection Results
echo ========================================
echo.
echo Opening result viewer in browser...
echo URL: http://localhost:7861
echo.
echo Press Ctrl+C to stop the server
echo.

cd /d "%~dp0"
python src\view_results.py

pause
