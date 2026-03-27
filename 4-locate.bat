@echo off
chcp 65001 >nul
echo ========================================
echo   Defect Location
echo ========================================
echo.

cd /d "%~dp0"

if not exist "models\defect_detection_resnet18.pth" (
    echo ERROR: Model not found!
    echo Please run "1-train.bat" first
    pause
    exit /b
)

set /p imgpath=Enter image path (e.g. data\bad\bad_0000_scratch.png): 

echo.
set /p gridsize=Grid size (default 4): 
if "%gridsize%"=="" set gridsize=4

echo.
echo Locating defect...
python src\locate_defect.py models\defect_detection_resnet18.pth %imgpath% %gridsize% 0.7

echo.
echo ========================================
echo Complete!
echo ========================================
echo.
pause
