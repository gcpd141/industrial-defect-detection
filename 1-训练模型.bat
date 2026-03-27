@echo off
chcp 65001 >nul
echo ========================================
echo   工业缺陷检测 - 训练模型
echo ========================================
echo.

cd /d "%~dp0"

echo [1/3] 检查数据...
if not exist "data\good" (
    echo 未找到数据集，正在生成...
    python src\generate_data.py data 100
) else (
    echo 数据集已存在，跳过生成
)

echo.
echo [2/3] 开始训练模型...
python src\train.py

echo.
echo [3/3] 训练完成！
echo 模型位置：models\defect_detection_resnet18.pth
echo.
pause
