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
- **Interactive Web Application & Cloud Deployment:** Deploy a full-stack web application (FastAPI + HTML5/CSS/JS) supporting photo upload, webcam capture, confidence thresholding, and visual side-by-side detection bounding boxes, hostable locally or deployed serverless on **Vercel** connected to Ultralytics Cloud Run inference.

## 📁 Repository Structure
```
ai-object-detection-ultralytics/
├── api/                                 # Vercel Serverless Function proxy
│   ├── index.py                         # Serverless FastAPI app (lightweight, connects to Cloud Run)
│   └── requirements.txt                 # Vercel dependencies (FastAPI, PIL, HTTPX - no heavy torch)
├── vercel.json                          # Vercel deployment routing and rewrites
├── mobile/                              # Cross-platform React Native & Expo mobile app (Android & iOS)
│   ├── App.js                           # Main application screen & navigation
│   ├── app.json                         # Expo mobile configuration & camera permissions
│   ├── package.json                     # Mobile app dependencies
│   ├── README.md                        # Mobile setup & Expo Go guide
│   └── src/
│       ├── config.js                    # API endpoints & constants
│       ├── services/api.js              # Camera upload & inference client
│       ├── styles/theme.js              # Dark slate / indigo UI theme tokens
│       └── components/                  # Header, ConfidenceSlider, ImagePreview, DetectionsList
├── webapp/                              # Full-stack object detection web application
│   ├── main.py                          # FastAPI backend with /predict and /health
│   ├── requirements.txt                 # Backend dependencies (with Ultralytics & PyTorch)
│   ├── .env.example                     # Environment configuration template
│   ├── README.md                        # Web application user guide
│   ├── model/
│   │   └── .gitkeep                     # Target folder for trained best.pt weights
│   └── static/
│       ├── index.html                   # Modern responsive UI
│       ├── style.css                    # Professional styles
│       └── app.js                       # Vanilla JS frontend & webcam controller
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

---

## 🌐 Deploy to Vercel (Online Cloud Hosting)

This project is fully configured for zero-configuration deployment on **Vercel**:

1. Go to [vercel.com/new](https://vercel.com/new) and log in with your GitHub account.
2. Under "Import Git Repository", find **`ai-object-detection-ultralytics`** and click **Import**.
3. Leave all default project settings as they are:
   - **Framework Preset:** *Other*
   - **Root Directory:** `./`
4. Click **Deploy**.
5. In ~30 seconds, your web application will be live at a public URL (e.g. `https://ai-object-detection-ultralytics.vercel.app`)!

> **How it works:** Vercel serves the responsive frontend and routes `/predict` and `/health` to `api/index.py`, which forwards requests to your dedicated Ultralytics Cloud Run inference endpoint and renders color-coded detection boxes using PIL.

---

## 📱 Running the Mobile App (iOS & Android)

A full-featured React Native & Expo mobile app is included in the `mobile/` directory:

1. Install **Expo Go** on your physical phone ([Google Play Store](https://play.google.com/store/apps/details?id=host.exp.exponent) or [iOS App Store](https://apps.apple.com/app/expo-go/id982107779)).
2. In your terminal, navigate to the `mobile` folder:
   ```bash
   cd mobile
   ```
3. Install dependencies:
   ```bash
   npm install
   ```
4. Start Expo:
   ```bash
   npm start
   ```
5. Scan the QR code with your phone (using Expo Go on Android or Camera app on iPhone) to test real-time camera inference!

---

## 🚀 Running the Web Application Locally

To run the interactive object detection web application locally:

1. Navigate into the `webapp` folder:
   ```bash
   cd webapp
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Place your trained weights (`best.pt`) into `webapp/model/best.pt`.
4. Start the server:
   ```bash
   uvicorn main:app --reload
   ```
5. Open your browser at **[http://localhost:8000](http://localhost:8000)**.

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
