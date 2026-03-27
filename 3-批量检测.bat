@echo off
chcp 65001 >nul
echo ========================================
echo   工业缺陷检测 - 批量检测
echo ========================================
echo.

cd /d "%~dp0"

if not exist "models\defect_detection_resnet18.pth" (
    echo ❌ 未找到模型文件！
    echo 请先运行 "1-训练模型.bat"
    pause
    exit /b
)

echo 开始批量检测...
echo.

python src\batch_detect.py models\defect_detection_resnet18.pth data detection_result 0.5

echo.
echo ========================================
echo 检测完成！
echo 结果查看：detection_result\
echo ========================================
echo.
pause
