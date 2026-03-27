# Industrial Defect Detection System

Deep learning-based industrial surface defect detection system with **single-image detection**, **batch detection**, and **defect location** features.

## 🎯 Features

- **Data Generation**: Simulated defect images or use real datasets
- **Model Training**: ResNet18 transfer learning
- **Single Image Detection**: Upload one image at a time
- **Batch Detection**: Detect entire folders, auto-classify, generate reports ⭐
- **Defect Location**: Mark defect positions for review ⭐

## 📦 Project Structure

```
industrial-defect-detection/
├── src/
│   ├── generate_data.py    # Data generation
│   ├── train.py            # Model training
│   ├── app.py              # Gradio web interface
│   ├── batch_detect.py     # Batch detection ⭐
│   └── locate_defect.py    # Defect location ⭐
├── data/                   # Dataset directory
├── models/                 # Trained models
├── detection_result/       # Batch detection results (auto-generated)
├── requirements.txt        # Python dependencies
├── start.bat              # Windows quick start menu
└── README.md              # This file
```

## 🚀 Quick Start (Windows)

### Option 1: Double-click to run (Recommended)

1. **Double-click** `start.bat`
2. **Enter number** to select function:
   - `[1]` Train Model (first time only)
   - `[2]` Web Detection Interface
   - `[3]` Batch Detection
   - `[4]` Defect Location

### Option 2: Command Line

```cmd
# 1. Install dependencies
pip install -r requirements.txt

# 2. Generate test data (or use your own)
cd src
python generate_data.py ..\data 100

# 3. Train model
python train.py

# 4. Web interface
python app.py
# Open browser: http://localhost:7860

# 5. Batch detection
python batch_detect.py models\defect_detection_resnet18.pth data detection_result 0.5

# 6. Defect location
python locate_defect.py models\defect_detection_resnet18.pth data\bad\bad_0000_scratch.png 4 0.7
```

## 📊 Results

After batch detection, you'll get:
- `detection_result\合格品\` - Good products
- `detection_result\缺陷品\` - Defective products  
- `detection_result\检测报告.md` - Detailed report

## 📋 Requirements

- Python 3.8+
- Windows 10/11 (or Linux/Mac)
- 4GB+ RAM
- Optional: NVIDIA GPU for faster training

## 🛠️ Dependencies

```
torch>=2.0.0
torchvision>=0.15.0
gradio>=4.0.0
opencv-python>=4.8.0
pillow>=10.0.0
numpy>=1.24.0
tqdm>=4.65.0
```

## 📝 Notes

- **First run**: Must train model first (run option 1 or `1-train.bat`)
- **Model location**: `models\defect_detection_resnet18.pth`
- **Threshold**: Default 0.5 (adjust based on your needs)

## 📄 License

MIT License

---

**Author**: Song Tao  
**Email**: 296068696@qq.com  
**GitHub**: https://github.com/GCPD141/industrial-defect-detection
