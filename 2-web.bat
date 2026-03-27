@echo off
chcp 65001 >nul
echo ========================================
echo   Web Detection Interface
echo ========================================
echo.
echo Open browser: http://localhost:7860
echo Press Ctrl+C to stop
echo.

cd /d "%~dp0"
python src\app.py

pause
