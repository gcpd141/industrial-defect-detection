#!/usr/bin/env python3
"""
工业缺陷检测演示界面
使用 Gradio 构建简单的上传 - 预测界面
"""

import gradio as gr
import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image
import numpy as np
from pathlib import Path

# 模型定义（与训练时一致）
class DefectClassifier(nn.Module):
    def __init__(self):
        super().__init__()
        model = models.resnet18(weights=None)
        num_features = model.fc.in_features
        model.fc = nn.Sequential(
            nn.Dropout(0.5),
            nn.Linear(num_features, 256),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(256, 2)
        )
        # 移除不需要的层，只保留特征提取和分类
        self.features = nn.Sequential(*list(model.children())[:-1])
        self.classifier = model.fc
    
    def forward(self, x):
        x = self.features(x)
        x = torch.flatten(x, 1)
        return self.classifier(x)

# 加载模型
MODEL_PATH = Path(__file__).parent.parent / 'models' / 'defect_detection_resnet18.pth'
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

def load_model():
    if MODEL_PATH.exists():
        model = DefectClassifier()
        checkpoint = torch.load(MODEL_PATH, map_location=device, weights_only=False)
        model.load_state_dict(checkpoint['model_state_dict'])
        model.to(device)
        model.eval()
        print(f"模型加载成功：{MODEL_PATH}")
        return model
    else:
        print(f"警告：模型文件不存在 {MODEL_PATH}")
        return None

model = load_model()

# 数据预处理
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

def predict_defect(image):
    """
    预测图片是否有缺陷
    """
    if model is None:
        return "❌ 模型未加载，请先运行训练", 0.0
    
    if image is None:
        return "请上传图片", 0.0
    
    # 预处理
    image_pil = Image.fromarray(image) if isinstance(image, np.ndarray) else image
    input_tensor = transform(image_pil).unsqueeze(0).to(device)
    
    # 预测
    with torch.no_grad():
        outputs = model(input_tensor)
        probabilities = torch.softmax(outputs, dim=1)[0]
        confidence = probabilities[1].item()  # 缺陷类的概率
    
    # 判断结果
    if confidence > 0.5:
        result = f"❌ **缺陷品** (置信度：{confidence:.2%})"
    else:
        result = f"✅ **合格品** (置信度：{1-confidence:.2%})"
    
    return result, confidence

# 创建 Gradio 界面
with gr.Blocks(title="工业缺陷检测系统", theme=gr.themes.Soft()) as demo:
    gr.Markdown("""
    # 🏭 工业缺陷检测系统
    
    上传零件图片，AI 自动检测是否存在缺陷（划痕、斑点、脏污、裂纹等）
    
    **适用场景**：金属表面检测、PCB 板检测、玻璃制品检测等
    """)
    
    with gr.Row():
        with gr.Column():
            input_image = gr.Image(label="上传零件图片", type="numpy")
            predict_btn = gr.Button("🔍 开始检测", variant="primary")
        
        with gr.Column():
            result_text = gr.Textbox(label="检测结果", lines=2)
            confidence_slider = gr.Slider(
                minimum=0, maximum=1, value=0,
                label="缺陷置信度", interactive=False
            )
    
    gr.Markdown("""
    ---
    ### 技术说明
    - 模型：ResNet18 迁移学习
    - 训练数据：模拟工业零件表面缺陷
    - 支持缺陷类型：划痕、斑点、脏污、裂纹
    
    ### 使用方法
    1. 点击"上传零件图片"或直接拖拽图片
    2. 点击"开始检测"
    3. 查看检测结果和置信度
    """)
    
    predict_btn.click(
        fn=predict_defect,
        inputs=input_image,
        outputs=[result_text, confidence_slider]
    )

if __name__ == '__main__':
    print("启动缺陷检测演示界面...")
    demo.launch(server_name='0.0.0.0', server_port=7860, share=False)
