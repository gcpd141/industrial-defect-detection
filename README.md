# 工业缺陷检测系统 (Industrial Defect Detection)

基于深度学习的工业表面缺陷检测系统，包含**单张检测**、**批量检测**、**缺陷定位**功能。

## 🎯 项目背景

工业视觉检测是 AI 落地的重要场景。传统方法依赖人工设计特征，深度学习可以自动学习缺陷特征。

本项目提供**完整的检测流程**：
- 数据生成/使用真实数据集
- 模型训练（ResNet18 迁移学习）
- 单张图片检测
- **批量检测**（一键检测整个文件夹，自动分类，生成报告）
- **缺陷定位**（标注缺陷位置，方便复核）

## 📦 项目结构

```
defect_detection/
├── src/
│   ├── generate_data.py    # 数据生成（模拟缺陷）
│   ├── train.py            # 模型训练
│   ├── app.py              # Gradio 单张检测界面
│   ├── batch_detect.py     # 批量检测脚本 ⭐
│   └── locate_defect.py    # 缺陷定位脚本 ⭐
├── data/                   # 数据集目录
├── models/                 # 训练好的模型
├── detection_result/       # 批量检测结果（自动生成）
├── requirements.txt        # Python 依赖
└── README.md               # 本文件
```

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 准备数据

**方式 A：使用模拟数据**
```bash
cd src
python generate_data.py ../data 100
```

**方式 B：使用真实数据集（推荐）**
```bash
# 下载东北大学带钢缺陷数据集
git clone https://github.com/GuoJaw/NEU-surface-defect-database.git
# 将数据集放到 data/ 目录
```

### 3. 训练模型

```bash
python train.py
```

训练完成后，模型保存至 `models/defect.pth`

### 4. 单张检测（Web 界面）

```bash
python app.py
```

浏览器访问 `http://localhost:7860`

### 5. 批量检测 ⭐

```bash
python batch_detect.py models/defect.pth data detection_result 0.5
```

**参数说明**：
- `models/defect.pth`: 模型路径
- `data`: 输入文件夹
- `detection_result`: 输出文件夹
- `0.5`: 缺陷判定阈值（默认 0.5）

**输出**：
- `detection_result/合格品/`: 合格图片
- `detection_result/缺陷品/`: 缺陷图片
- `detection_result/检测报告.md`: 详细检测报告

### 6. 缺陷定位 ⭐

```bash
python locate_defect.py models/defect.pth data/bad/0.png 4 0.7
```

**参数说明**：
- `4`: 网格大小（4x4）
- `0.7`: 缺陷判定阈值

**输出**：标注缺陷位置的图片（`xxx_annotated.png`）

## 📊 技术细节

### 模型架构

- **骨干网络**：ResNet18（ImageNet 预训练）
- **分类头**：Dropout + FC(256) + ReLU + Dropout + FC(2)
- **输入尺寸**：224×224 RGB

### 训练配置

| 超参数 | 值 |
|--------|-----|
| Batch Size | 16 |
| 学习率 | 0.001 |
| 优化器 | Adam |
| Epochs | 20 |

### 数据增强

- 随机水平翻转
- 随机旋转（±10°）
- 颜色抖动（亮度、对比度）

## 📈 效果

| 数据集 | 准确率 | 说明 |
|--------|--------|------|
| 模拟数据 | 90%+ | 程序生成的缺陷 |
| 东北大学带钢 | 60-80% | 真实工业数据，噪声大 |

**注意**：真实场景需要现场调试、数据增强、模型优化。

## 💡 工业场景功能

### 批量检测

**解决什么问题**：
- 工厂不是一张一张检测，是**一批一批检测**
- 检测完要**出报告**（合格率、缺陷类型分布）
- 缺陷品要**分类存放**

**功能**：
- ✅ 一键检测整个文件夹
- ✅ 自动分类存放（合格品/缺陷品）
- ✅ 生成 Markdown 检测报告
- ✅ 支持阈值调整

### 缺陷定位

**解决什么问题**：
- 不仅要知道"有没有缺陷"
- 还要知道"**缺陷在哪里**"
- 方便质检员**复核**

**功能**：
- ✅ 滑动窗口定位（简易版）
- ✅ 标注缺陷区域
- ✅ 输出标注图片

**工业场景升级方向**：
- Grad-CAM 热力图
- YOLO/Faster R-CNN 检测模型
- 像素级分割（U-Net）

## 🎓 学习价值

通过本项目，可以展示：

1. **数据处理**：理解工业缺陷检测的数据特点
2. **迁移学习**：使用预训练模型解决小样本问题
3. **模型训练**：完整的训练流程和调参经验
4. **工程能力**：从数据到部署的完整 pipeline
5. **工业思维**：批量检测、缺陷定位、报告生成

## 📝 后续扩展方向

1. **真实数据**：采集产线图片，重新训练
2. **多分类**：区分不同缺陷类型（划痕/斑点/裂纹等）
3. **缺陷检测**：从分类升级为检测（YOLO）
4. **模型压缩**：ONNX/TensorRT 部署优化
5. **实时检测**：集成摄像头，实时拍摄实时识别
6. **数据管道**：自动采集产线数据，持续迭代

## 📄 许可证

MIT License

---

**作者**：宋涛  
**日期**：2026.03  
**联系**：296068696@qq.com  
**GitHub**：github.com/GCPD141/industrial-defect-detection
