@echo off
chcp 65001 >nul
echo ========================================
echo   Train Model
echo ========================================
echo.

cd /d "%~dp0"

echo [1/3] Checking data...
if not exist "data\good" (
    echo No dataset found, generating...
    python src\generate_data.py data 100
) else (
    echo Dataset exists, skipping
)

echo.
echo [2/3] Training model...
python src\train.py

echo.
echo [3/3] Training complete!
echo Model saved to: models\defect_detection_resnet18.pth
echo.
pause
