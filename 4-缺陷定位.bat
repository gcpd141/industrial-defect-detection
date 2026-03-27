@echo off
chcp 65001 >nul
echo ========================================
echo   工业缺陷检测 - 缺陷定位
echo ========================================
echo.

cd /d "%~dp0"

if not exist "models\defect_detection_resnet18.pth" (
    echo ❌ 未找到模型文件！
    echo 请先运行 "1-训练模型.bat"
    pause
    exit /b
)

echo 请输入要定位的图片路径 (例如：data\bad\bad_0000_scratch.png)
set /p imgpath=图片路径：

echo.
echo 请输入网格大小 (默认 4)
set /p gridsize=网格大小：
if "%gridsize%"=="" set gridsize=4

echo.
echo 开始定位...
python src\locate_defect.py models\defect_detection_resnet18.pth %imgpath% %gridsize% 0.7

echo.
echo ========================================
echo 定位完成！
echo ========================================
echo.
pause
