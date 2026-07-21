# 🌊 AI-Based Plastic, Oil Spill & Microalgae Detection

<p align="center">

![Python](https://img.shields.io/badge/Python-3.13-blue)
![YOLOv9](https://img.shields.io/badge/YOLO-v9-red)
![Flask](https://img.shields.io/badge/Flask-Web_App-black)
![OpenCV](https://img.shields.io/badge/OpenCV-Computer_Vision-green)
![Deep Learning](https://img.shields.io/badge/Deep_Learning-YOLO-orange)
![License](https://img.shields.io/badge/License-MIT-brightgreen)

</p>

---

# 📖 Overview

This project presents an **AI-powered environmental hazard detection system** capable of detecting **Plastic Waste**, **Oil Spills**, and **Microalgae** from aerial and marine images using state-of-the-art **YOLO object detection models**.

The system provides a **real-time web interface** where users can upload images, perform automatic pollutant detection, visualize detected objects with bounding boxes, generate reports, and interact using **voice commands**.

The project was developed as part of our IEEE research work on **Deep Learning for Environmental Hazard Detection using YOLO**.

---

# ✨ Features

- 🌊 Plastic Waste Detection
- 🛢️ Oil Spill Detection
- 🌿 Microalgae Detection
- 🤖 YOLOv8, YOLOv9 & YOLOv11 Comparison
- 📷 Image Upload Detection
- 🎯 Real-time Object Detection
- 📊 Detection Confidence Scores
- 📝 Report Generation
- 🗂️ SQLite Database Integration
- 🌐 Responsive Flask Web Application
- 🎙️ Voice Assistant Support
- 👤 User Login & Registration System

---

# 🧠 Models Used

- YOLOv8s
- YOLOv9s
- YOLOv11s

The project compares all three models under identical experimental conditions to evaluate:

- Precision
- Recall
- F1 Score
- mAP@50
- mAP@50-95

---

# 🏗️ Project Architecture

```
                User
                  │
                  ▼
          Flask Web Interface
                  │
      ┌───────────┴───────────┐
      ▼                       ▼
 Image Upload          Voice Assistant
      │                       │
      └──────────────┬────────┘
                     ▼
           YOLO Detection Model
                     │
                     ▼
    Plastic | Oil Spill | Microalgae
                     │
                     ▼
         Bounding Box Prediction
                     │
                     ▼
          Detection Results
                     │
                     ▼
          SQLite Database
                     │
                     ▼
          Report Generation
```

---

# 📂 Project Structure

```
CODE
│
├── BACKEND
│   ├── MODEL.ipynb
│   ├── YOLO Models
│   └── Training Files
│
├── FRONTEND
│   ├── app.py
│   ├── templates
│   ├── static
│   ├── uploads
│   └── db.sql
│
└── README.md
```

---

# 🚀 Technologies Used

- Python
- Flask
- OpenCV
- Ultralytics YOLO
- SQLite
- HTML
- CSS
- JavaScript
- Bootstrap
- Jupyter Notebook

---

# 📊 Datasets

The project uses three publicly available datasets.

- Plastic Waste Dataset
- Oil Spill Dataset
- Microalgae Dataset

Images are resized to **640×640** before training.

---

# 📈 Results

| Dataset | Best Model | mAP@50 | Precision |
|----------|-----------|---------|-----------|
| Plastic Waste | YOLOv8s | 55.66 | 70.51% |
| Oil Spill | YOLOv9s | **97.00** | **92.90%** |
| Microalgae | YOLOv9s | 63.90 | 87.70% |

YOLOv9 achieved the best overall performance for environmental hazard detection.
##🏆 Highlights

- 🎯 **97.00% mAP@50** on Oil Spill Detection
- 🎯 **92.90% Precision** on Oil Spill Detection
- 🎯 **94.20% Recall** on Oil Spill Detection
- 🎯 **93.55% F1-Score** on Oil Spill Detection
- 🎯 **81.75% Detection Accuracy** on Oil Spill Detection
- 🌊 Real-time multi-pollutant detection using a unified YOLO-based framework
- ⚡ Optimized for deployment through a Flask web application
---

# 💻 Web Application

The Flask web application provides

- User Authentication
- Image Upload
- Real-time Detection
- Detection Visualization
- Voice Assistant
- Result Storage
- Report Generation

---

# 📷 Sample Outputs

## Plastic Waste Detection

![Plastic Detection](assets/plastic_detection.png)

---

## Oil Spill Detection

![Oil Spill](assets/oil_spill_detection.png)

---

## Microalgae Detection

![Microalgae](assets/microalgae_detection.png)

---

# ⚙️ Installation

Clone the repository

```bash
git clone https://github.com/yourusername/AI-Plastic-Oil-Microalgae-Detection.git
```

Move into the project

```bash
cd AI-Plastic-Oil-Microalgae-Detection
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the application

```bash
python app.py
```

---

# 📄 License

This project is intended for academic and research purposes.
