# 🎯 AI Object Detection Web Application (Ultralytics YOLO)

A lightweight, modern web application for running real-time object detection and facial/personal recognition using custom-trained **Ultralytics YOLO** models.

---

## 📌 What This App Does
- **Photo Upload:** Drag-and-drop or browse an image file (`.jpg`, `.jpeg`, `.png`, `.webp` up to 10 MB) to detect persons or custom objects.
- **Webcam Mode:** Use your laptop or phone camera to capture a live photo and run inference instantly.
- **Interactive Confidence Slider:** Adjust detection sensitivity between 5% and 95% in real time.
- **Side-by-Side Visual Comparison:** Inspect the original photo next to the YOLO annotated image with color-coded bounding boxes and confidence labels.
- **Detailed Detections Breakdown:** Review detected classes, confidence scores (%), and bounding box coordinates `[x1, y1, x2, y2]`.
- **Result Download:** Save and download the annotated detection output with one click.
- **Ultralytics HUB Support:** Seamlessly switch to cloud-hosted Ultralytics HUB API inference using environment variables.

---

## 📸 Screenshots & UI Preview

```
+---------------------------------------------------------------------------------------+
|  🎯 AI Object Detection - Ultralytics                     [● Model Ready (1 class)]   |
+---------------------------------------+-----------------------------------------------+
|  1. INPUT SOURCE & SETTINGS           |  2. VISUAL DETECTIONS     [Download Result]   |
|  [ Upload Photo ]  [ Use Webcam ]     |  Found: 3 | Time: 42.1 ms | Dim: 1280x720     |
|                                       |                                               |
|  +---------------------------------+  |  +-------------------+  +-------------------+ |
|  |     Drag & drop photo here      |  |  |  Original Image   |  | YOLO Detection    | |
|  |     or click to browse          |  |  |  [User photo]     |  | [Bounding Box]    | |
|  +---------------------------------+  |  +-------------------+  +-------------------+ |
|                                       |                                               |
|  Confidence Threshold: 25%            |  Detections Breakdown:                        |
|  [-------●-----------------------]    |  #1  Isaac   96.4%  [120.4, 45.2, 380.1, 490] |
|                                       |  #2  Person  88.1%  [410.0, 60.5, 620.4, 510] |
|  [ Run YOLO Detection ]               |                                               |
+---------------------------------------+-----------------------------------------------+
```

---

## 🚀 Quick Start Guide

### Step 1: Open a Terminal
Navigate to the `webapp` folder:
```bash
cd webapp
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Add Your Trained Model Weights
Copy your custom-trained YOLO weights file (`best.pt`) into the `model/` folder:
```
webapp/
└── model/
    └── best.pt    <-- Place your trained weights file here
```
*(If you want to use a model located elsewhere, you can set the `MODEL_PATH` environment variable).*

### Step 4: Start the Web Application
Run:
```bash
uvicorn main:app --reload
```
or:
```bash
python main.py
```

### Step 5: Open in Your Browser
Open your browser and visit:
👉 **[http://localhost:8000](http://localhost:8000)**

---

## ⚙️ Configuration & Environment Variables

Copy `.env.example` to `.env` to customize settings:

| Variable | Default | Description |
| :--- | :--- | :--- |
| `MODEL_PATH` | `model/best.pt` | Path to your local YOLO weights file (`.pt`). |
| `HOST` | `0.0.0.0` | Server bind address. |
| `PORT` | `8000` | Port to run the server on. |
| `USE_HUB_API` | `false` | Set to `true` to use Ultralytics HUB API instead of local model. |
| `HUB_API_KEY` | *(empty)* | Your Ultralytics HUB API Key. |
| `HUB_MODEL_URL`| `https://api.ultralytics.com/v1/predict` | Ultralytics HUB Inference endpoint. |

---

## 📡 API Endpoints

The FastAPI backend exposes the following endpoints:

### 1. Health Check
- **`GET /health`**
- **Description:** Checks if the server is healthy and if model weights are loaded.
- **Response Example:**
  ```json
  {
    "status": "healthy",
    "model_loaded": true,
    "model_path": "model/best.pt",
    "use_hub_api": false,
    "class_names": {
      "0": "Isaac"
    },
    "classes_count": 1,
    "message": "Model is loaded and ready for predictions."
  }
  ```

### 2. Predict / Object Detection
- **`POST /predict`**
- **Content-Type:** `multipart/form-data`
- **Parameters:**
  - `file`: The image file (JPEG, PNG, or WebP; maximum 10 MB).
  - `conf`: Confidence threshold float between `0.05` and `0.95` (default: `0.25`).
- **Response Example:**
  ```json
  {
    "image_width": 1280,
    "image_height": 720,
    "detections": [
      {
        "class_name": "Isaac",
        "confidence": 0.9421,
        "bbox": [120.4, 45.2, 380.1, 490.5]
      }
    ],
    "count": 1,
    "inference_ms": 38.45,
    "annotated_image": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQ..."
  }
  ```

### 3. Frontend App
- **`GET /`**
- **Description:** Serves the responsive single-page HTML/CSS/JavaScript web interface.

---

## 🌐 Deploy Online on Vercel

You can host this application completely free on **Vercel** without running any servers locally:

1. Push this repository to your GitHub account (`ai-object-detection-ultralytics`).
2. Log in at [vercel.com](https://vercel.com) and click **"Add New Project"**.
3. Import your `ai-object-detection-ultralytics` repository.
4. Keep the default settings (Framework: *Other*, Root Directory: `./`) and click **Deploy**.
5. Once deployed, open your live Vercel URL to upload photos or use your webcam directly from your smartphone or laptop!

---

## 🧪 How to Test

### Automated curl Test
```bash
curl -X POST "http://localhost:8000/predict" \
  -F "file=@path/to/test_photo.jpg" \
  -F "conf=0.25"
```

### Interactive UI Test
1. Start the server with `uvicorn main:app --reload`.
2. Open `http://localhost:8000` in Google Chrome or Edge.
3. Drag and drop any photo of yourself or a group.
4. Click **Run YOLO Detection** and verify the predicted bounding boxes, labels, and table metrics.
5. Switch to **Use Webcam**, click **Turn On Camera**, and test real-time capture.
