@echo off
chcp 65001 >nul
echo ========================================
echo   Batch Detection
echo ========================================
echo.

cd /d "%~dp0"

if not exist "models\defect_detection_resnet18.pth" (
    echo ERROR: Model not found!
    echo Please run "1-train.bat" first
    pause
    exit /b
)

echo Starting batch detection...
echo.

python src\batch_detect.py models\defect_detection_resnet18.pth data detection_result 0.5

echo.
echo ========================================
echo Complete!
echo Results: detection_result\
echo ========================================
echo.
pause
