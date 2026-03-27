@echo off
chcp 65001 >nul
title Industrial Defect Detection - Batch Detection
cls

echo ========================================
echo   Batch Detection
echo ========================================
echo.

cd /d "%~dp0"

REM 检查模型是否存在
if not exist "models\defect_detection_resnet18.pth" (
    echo ERROR: Model not found!
    echo Please run "1-train.bat" first.
    echo.
    pause
    exit /b 1
)

echo Starting batch detection...
echo.

python src\batch_detect.py models\defect_detection_resnet18.pth data detection_result 0.5

echo.
echo ========================================
echo Complete!
echo ========================================
echo.
echo Results saved to: detection_result\
echo.
echo Do you want to view results in browser?
echo.
set /p open=Open result viewer now? (Y/N): 

if /i "%open%"=="Y" (
    echo.
    echo Opening result viewer...
    echo.
    start "" "5-view.bat"
)

echo.
echo Press any key to exit...
pause >nul
