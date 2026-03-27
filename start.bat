@echo off
chcp 65001 >nul
echo ========================================
echo   Industrial Defect Detection - Menu
echo ========================================
echo.
echo Select an option:
echo.
echo   [1] Train Model (first time only)
echo   [2] Web Detection Interface
echo   [3] Batch Detection
echo   [4] Defect Location
echo   [0] Exit
echo.
set /p choice=Enter choice (0-4): 

if "%choice%"=="1" start "" "1-train.bat"
if "%choice%"=="2" start "" "2-web.bat"
if "%choice%"=="3" start "" "3-batch.bat"
if "%choice%"=="4" start "" "4-locate.bat"
if "%choice%"=="0" exit

echo.
pause
