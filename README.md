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
- **AI Foundations Practice:** Build core machine learning and generative AI competencies, including regression modeling, local LLM deployment with Ollama, and full coursework progression.

## 📁 Repository Structure
```
ai-object-detection-ultralytics/
├── notebooks/
│   ├── coursework/                      # University coursework (migrated from Google Colab)
│   │   ├── 01_python_basics_variables_and_loops.ipynb
│   │   ├── 02_python_functions_oop_and_modules.ipynb
│   │   └── 03_classification_logistic_regression_and_evaluation.ipynb
│   └── practice/                        # Class preparation & foundational practice
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
   pip install ultralytics scikit-learn matplotlib pandas seaborn ollama
   ```

---

## 📖 Coursework Notebooks (Google Colab)
Located in `notebooks/coursework/`:

1. **`01_python_basics_variables_and_loops.ipynb`**
   - **Topics:** Python variables, data types (int, float, string, boolean), arithmetic & logical operators, `for` and `while` loops, basic OOP `Dog` class, functions, and module importing.
   - **Original Colab:** [Open in Google Colab](https://colab.research.google.com/drive/1hIT3c6TvtjjPzeRDR_Z5OxvKO-t8X3H7?usp=sharing)

2. **`02_python_functions_oop_and_modules.ipynb`**
   - **Topics:** Functions with positional, keyword, and default parameters; advanced string formatting (f-strings and `.format()`); Object-Oriented Programming (inheritance, method overriding vs. extension, `super()`); and multi-file module organization (`__name__ == "__main__"`).
   - **Original Colab:** [Open in Google Colab](https://colab.research.google.com/drive/1PaG071uGbGkgznhyYbcJCSVi36LvYh_X?usp=sharing)

3. **`03_classification_logistic_regression_and_evaluation.ipynb`**
   - **Topics:** Complete classification lab using the Pima Indians Diabetes dataset. Covers conceptual foundations, feature scaling with `StandardScaler`, Logistic Regression modeling, probability prediction, decision boundaries, ROC curves with AUC score, threshold tuning (0.3 vs 0.5 vs 0.7), Confusion Matrix visualization, Scikit-Learn classification reports, and Precision-Recall trade-off analysis.
   - **Original Colab:** [Open in Google Colab](https://colab.research.google.com/drive/1aQ6Bo9861bCmH8cjBRr9JvKQI-UAR-oF?usp=sharing)

---

## 📚 Practice Notebooks
Located in `notebooks/practice/`:

1. **`ollama_llama32_demo.ipynb`**: Demonstrates running and prompting Meta's Llama 3.2 1B model locally on CPU via Ollama's Python client with streaming and chat history.
2. **`linear_regression.ipynb`**: Supervised learning predicting house prices from square footage with best-fit line visualization ($R^2$ & MSE).
3. **`logistic_regression.ipynb`**: Binary classification predicting student exam pass/fail from study hours, featuring the Sigmoid curve, Confusion Matrix, Accuracy, Precision, and Recall.
