@echo off
chcp 65001 >nul
title Industrial Defect Detection - Result Viewer
cls

echo ========================================
echo   View Detection Results
echo ========================================
echo.
echo Starting web server...
echo.
echo After server starts, open browser:
echo http://localhost:7861
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.

cd /d "%~dp0"

REM 检查 Python 是否存在
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found!
    echo Please install Python first.
    pause
    exit /b 1
)

REM 检查 view_results.py 是否存在
if not exist "src\view_results.py" (
    echo ERROR: view_results.py not found!
    echo Please make sure you downloaded the complete project.
    pause
    exit /b 1
)

REM 启动服务器
python src\view_results.py

pause
