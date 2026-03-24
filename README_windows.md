# Windows 用户运行指南

## 检查环境

```cmd
python --version
pip list | findstr "torch gradio opencv"
```

## 安装依赖

```cmd
pip install torch torchvision gradio opencv-python pillow numpy tqdm
```

## 运行项目

```cmd
cd defect_detection

REM 1. 生成数据集
cd src
python generate_data.py ..\data 100

REM 2. 训练模型
python train.py

REM 3. 启动演示界面
python app.py
```

浏览器访问：http://localhost:7860
