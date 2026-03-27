# Industrial Defect Detection System

Deep learning-based industrial surface defect detection system with **web interface** for viewing results.

## 🎯 Features

- **Data Generation**: Simulated defect images or use real datasets
- **Model Training**: ResNet18 transfer learning
- **Single Image Detection**: Upload one image at a time via web
- **Batch Detection**: Detect entire folders, auto-classify, generate reports ⭐
- **Defect Location**: Mark defect positions for review ⭐
- **Result Viewer**: **Web gallery to view and share results** ⭐NEW!

## 📦 Project Structure

```
industrial-defect-detection/
├── src/
│   ├── generate_data.py    # Data generation
│   ├── train.py            # Model training
│   ├── app.py              # Gradio web interface (single detection)
│   ├── batch_detect.py     # Batch detection ⭐
│   ├── locate_defect.py    # Defect location ⭐
│   └── view_results.py     # Result viewer (web gallery) ⭐NEW!
├── data/                   # Dataset directory
├── models/                 # Trained models
├── detection_result/       # Batch detection results (auto-generated)
├── requirements.txt        # Python dependencies
├── start.bat              # Windows quick start menu
└── README.md              # This file
```

## 🚀 Quick Start (Windows)

### Step-by-Step Guide

#### 1️⃣ First Time Setup (Do this once)

**Double-click**: `1-train.bat`

This will:
- Generate test data (if needed)
- Train the AI model
- Save model to `models\defect_detection_resnet18.pth`

⏱️ Takes about 5-10 minutes. **Only needed once!**

---

#### 2️⃣ Run Batch Detection

**Double-click**: `3-batch.bat`

This will:
- Detect all images in `data\` folder
- Sort into `合格品\` (good) and `缺陷品\` (defective)
- Generate report
- **Automatically open result viewer in browser!** 🎉

---

#### 3️⃣ View Results in Browser

After batch detection completes, your browser will open automatically at:
```
http://localhost:7861
```

**Or manually**: Double-click `5-view.bat`

**What you'll see**:
- 📊 Statistics (total count, pass/fail rates)
- 📋 Detailed report
- 🖼️ **Image gallery** (browse all results)
- 📤 **Easy to share** - just show the browser window!

---

#### 4️⃣ Other Options

| File | What it does | When to use |
|------|-------------|-------------|
| `2-web.bat` | Single image detection | Test one image at a time |
| `4-locate.bat` | Mark defect location | Show exactly where defect is |
| `5-view.bat` | View results gallery | Show results to others |

---

## 🖼️ Result Viewer Features

The web viewer (`5-view.bat`) provides:

### Tab 1: 📊 Statistics Overview
- Total count
- Pass/fail numbers and percentages
- Full detection report

### Tab 2: 🖼️ Image Gallery
- Browse all **good products**
- Browse all **defective products**
- Grid view (4 columns)
- Image names displayed

### Perfect for:
- ✅ Showing results to colleagues
- ✅ Presenting to clients
- ✅ Quality review meetings
- ✅ Sharing via screen share

---

## 📊 Example Output

After running batch detection:

```
detection_result/
├── 合格品/           ← Good products (20 images)
├── 缺陷品/           ← Defective products (20 images)
└── 检测报告.md       ← Detailed report
```

**To view**: 
- Option A: Open browser → `http://localhost:7861` (recommended)
- Option B: Open `detection_result\检测报告.md` in browser

---

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

## 💡 Workflow Summary

```
1st time: 1-train.bat → Wait 5-10 min → Model ready ✅

Every time after:
1. Put your images in data\ folder
2. Double-click 3-batch.bat
3. Browser opens automatically
4. Show results to others! 🎉
```

## 📄 License

MIT License

---

**Author**: Song Tao  
**Email**: 296068696@qq.com  
**GitHub**: https://github.com/GCPD141/industrial-defect-detection
