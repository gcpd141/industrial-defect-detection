@echo off
chcp 65001 >nul
title Industrial Defect Detection - Menu
cls

:menu
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
echo   [5] View Results
echo   [0] Exit
echo.
set /p choice=Enter choice (0-5): 

if "%choice%"=="1" call :run "1-train.bat"
if "%choice%"=="2" call :run "2-web.bat"
if "%choice%"=="3" call :run "3-batch.bat"
if "%choice%"=="4" call :run "4-locate.bat"
if "%choice%"=="5" call :run "5-view.bat"
if "%choice%"=="0" exit

goto menu

:run
start "" %1
goto :eof
