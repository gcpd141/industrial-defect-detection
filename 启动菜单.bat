@echo off
chcp 65001 >nul
echo ========================================
echo   工业缺陷检测系统 - 快速开始
echo ========================================
echo.
echo 请选择要执行的操作：
echo.
echo   [1] 训练模型 (首次运行必做)
echo   [2] 启动 Web 检测界面
echo   [3] 批量检测
echo   [4] 缺陷定位
echo   [0] 退出
echo.
set /p choice=请输入选项 (0-4)：

if "%choice%"=="1" start "" "1-训练模型.bat"
if "%choice%"=="2" start "" "2-Web 检测界面.bat"
if "%choice%"=="3" start "" "3-批量检测.bat"
if "%choice%"=="4" start "" "4-缺陷定位.bat"
if "%choice%"=="0" exit

echo.
pause
