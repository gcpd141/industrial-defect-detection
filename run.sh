#!/bin/bash
# 工业缺陷检测 Demo 一键运行脚本

set -e

echo "========================================="
echo "  工业缺陷检测 Demo - 一键运行"
echo "========================================="

cd "$(dirname "$0")"

# 检查依赖
echo ""
echo "📦 检查依赖..."
python -c "import torch, gradio, cv2" 2>/dev/null || {
    echo "❌ 缺少依赖，正在安装..."
    pip install -r requirements.txt
}

# 检查数据集
if [ ! -d "data/good" ] || [ ! -d "data/bad" ]; then
    echo ""
    echo "📊 生成数据集..."
    cd src
    python generate_data.py ../data 100
    cd ..
fi

# 检查模型
if [ ! -f "models/defect_detection_resnet18.pth" ]; then
    echo ""
    echo "🧠 训练模型..."
    cd src
    python train.py
    cd ..
fi

# 启动界面
echo ""
echo "🚀 启动演示界面..."
echo "浏览器访问：http://localhost:7860"
echo ""
cd src
python app.py
