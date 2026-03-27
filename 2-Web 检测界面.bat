@echo off
chcp 65001 >nul
echo ========================================
echo   工业缺陷检测 - Web 界面
echo ========================================
echo.
echo 启动后浏览器访问：http://localhost:7860
echo 按 Ctrl+C 停止服务
echo.

cd /d "%~dp0"
python src\app.py

pause
