# AI Object Detection & Recognition with Ultralytics YOLO

**Course:** Artificial Intelligence  
**Institution:** Pentecost University College  

---

## 📌 Project Overview
This project focuses on building a custom computer vision pipeline for real-time object detection and facial/personal recognition using **Ultralytics YOLO** (You Only Look Once). The core goal is to train and evaluate a YOLO model capable of detecting and accurately recognizing myself in real-time camera feeds and recorded video.

## 🎯 Objectives
- **Data Collection & Annotation:** Gather diverse image samples under varying lighting conditions, angles, and backgrounds, annotating bounding boxes for custom classes.
- **Model Training:** Fine-tune pre-trained Ultralytics YOLO models on custom annotated datasets.
- **Inference & Evaluation:** Benchmark precision, recall, and mAP (mean Average Precision) for real-time detection on CPU/GPU.
- **AI Foundations Practice:** Build core machine learning and generative AI competencies, including regression modeling and local LLM deployment with Ollama.

## 📁 Repository Structure
```
ai-object-detection-ultralytics/
├── notebooks/
│   └── practice/
│       ├── ollama_llama32_demo.ipynb    # Local LLM prompting with Ollama & Llama 3.2 1B
│       ├── linear_regression.ipynb      # House price prediction with Scikit-Learn
│       └── logistic_regression.ipynb    # Pass/fail prediction with confusion matrix & metrics
├── .gitignore                           # Ignores venvs, raw images, and large weights (.pt)
└── README.md                            # Project overview and documentation
```

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- [Ollama](https://ollama.com/) (for local LLM tasks)
- Git

### Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/nkansahisaac436-dotcom/ai-object-detection-ultralytics.git
   cd ai-object-detection-ultralytics
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install ultralytics scikit-learn matplotlib ollama
   ```

## 📚 Practice Notebooks
Inside `notebooks/practice/`:
1. **`ollama_llama32_demo.ipynb`**: Demonstrates running and prompting Meta's Llama 3.2 1B model locally on CPU via Ollama's Python client.
2. **`linear_regression.ipynb`**: Introduces basic supervised learning by predicting house prices based on square footage.
3. **`logistic_regression.ipynb`**: Demonstrates binary classification predicting student exam pass/fail from study hours, featuring Confusion Matrix, Accuracy, Precision, and Recall.
