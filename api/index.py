import os
import io
import time
import base64
import logging
from pathlib import Path
from typing import Optional, Dict, Any, List

from fastapi import FastAPI, File, UploadFile, Form, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from PIL import Image
import httpx

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("vercel_api")

app = FastAPI(
    title="AI Object Detection - Vercel Serverless API",
    description="Vercel Serverless Function proxy for YOLO Object Detection & Personal Recognition",
    version="1.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Environment variables
USE_HUB_API = os.getenv("USE_HUB_API", "false").lower() in ("true", "1", "yes")
HUB_API_KEY = os.getenv("HUB_API_KEY", "")
HUB_MODEL_URL = os.getenv("HUB_MODEL_URL", "https://api.ultralytics.com/v1/predict")
REMOTE_BACKEND_URL = os.getenv("REMOTE_BACKEND_URL", "").rstrip("/")
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

# Check if local YOLO is available
try:
    from ultralytics import YOLO
    LOCAL_YOLO_AVAILABLE = True
except ImportError:
    LOCAL_YOLO_AVAILABLE = False


@app.get("/health")
@app.get("/api/health")
def health_check() -> Dict[str, Any]:
    """Health check endpoint for Vercel deployment."""
    is_ready = USE_HUB_API or bool(REMOTE_BACKEND_URL) or LOCAL_YOLO_AVAILABLE

    message = "Vercel API is live."
    if USE_HUB_API:
        message = "Connected to Ultralytics HUB Cloud API."
    elif REMOTE_BACKEND_URL:
        message = f"Proxying inference to remote backend: {REMOTE_BACKEND_URL}"
    elif LOCAL_YOLO_AVAILABLE:
        message = "Local YOLO model engine available."
    else:
        message = (
            "Vercel frontend is ready! To enable cloud inference on Vercel, set "
            "USE_HUB_API=true and HUB_API_KEY in your Vercel Project Settings, "
            "or set REMOTE_BACKEND_URL pointing to your Render/Railway backend."
        )

    return {
        "status": "healthy" if is_ready else "setup_needed",
        "platform": "vercel_serverless",
        "model_loaded": is_ready,
        "use_hub_api": USE_HUB_API,
        "remote_backend_configured": bool(REMOTE_BACKEND_URL),
        "local_yolo_available": LOCAL_YOLO_AVAILABLE,
        "message": message
    }


@app.post("/predict")
@app.post("/api/predict")
async def predict(
    file: UploadFile = File(..., description="Image file (JPEG, PNG, or WebP)"),
    conf: float = Form(0.25, description="Confidence threshold between 0.05 and 0.95")
):
    """Run prediction either via HUB API, remote backend, or local YOLO."""
    # 1. Validate file
    allowed_extensions = {".jpg", ".jpeg", ".png", ".webp"}
    file_ext = Path(file.filename or "").suffix.lower()
    content_type = (file.content_type or "").lower()

    if file_ext not in allowed_extensions and not content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file type. Please upload a valid image (JPEG, PNG, or WebP)."
        )

    contents = await file.read()
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File size exceeds 10 MB limit ({len(contents) / (1024*1024):.2f} MB received)."
        )

    if len(contents) == 0:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    conf_clamped = max(0.05, min(0.95, float(conf)))

    # Option A: Ultralytics HUB API
    if USE_HUB_API:
        if not HUB_API_KEY:
            raise HTTPException(
                status_code=500,
                detail="HUB_API_KEY environment variable is not configured on Vercel."
            )
        headers = {"x-api-key": HUB_API_KEY}
        files = {"file": (file.filename or "image.jpg", contents, "image/jpeg")}
        data = {"conf": str(conf_clamped)}

        start_time = time.perf_counter()
        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                resp = await client.post(HUB_MODEL_URL, headers=headers, files=files, data=data)
                resp.raise_for_status()
                hub_json = resp.json()
            except Exception as e:
                raise HTTPException(status_code=502, detail=f"HUB API error: {str(e)}")

        inference_ms = round((time.perf_counter() - start_time) * 1000, 2)
        return {
            "image_width": hub_json.get("image_width", 0),
            "image_height": hub_json.get("image_height", 0),
            "detections": hub_json.get("detections", []),
            "count": len(hub_json.get("detections", [])),
            "inference_ms": inference_ms,
            "annotated_image": hub_json.get("annotated_image", "")
        }

    # Option B: Forward to Remote Dedicated Backend (Render / Railway / Hugging Face)
    if REMOTE_BACKEND_URL:
        endpoint = f"{REMOTE_BACKEND_URL}/predict"
        files = {"file": (file.filename or "image.jpg", contents, "image/jpeg")}
        data = {"conf": str(conf_clamped)}

        start_time = time.perf_counter()
        async with httpx.AsyncClient(timeout=45.0) as client:
            try:
                resp = await client.post(endpoint, files=files, data=data)
                resp.raise_for_status()
                return resp.json()
            except Exception as e:
                raise HTTPException(
                    status_code=502,
                    detail=f"Failed to communicate with remote backend at {endpoint}: {str(e)}"
                )

    # Option C: Local YOLO (if torch & ultralytics are installed in the environment)
    if LOCAL_YOLO_AVAILABLE:
        from webapp.main import yolo_model, model_loaded
        if yolo_model is not None:
            pil_image = Image.open(io.BytesIO(contents)).convert("RGB")
            t0 = time.perf_counter()
            results = yolo_model.predict(source=pil_image, conf=conf_clamped, verbose=False)
            elapsed_ms = round((time.perf_counter() - t0) * 1000, 2)
            result = results[0]

            detections = []
            if result.boxes is not None:
                for box in result.boxes:
                    cls_id = int(box.cls[0].item())
                    cls_name = result.names.get(cls_id, str(cls_id))
                    conf_score = round(float(box.conf[0].item()), 4)
                    coords = [round(float(c), 1) for c in box.xyxy[0].tolist()]
                    detections.append({"class_name": cls_name, "confidence": conf_score, "bbox": coords})

            # Plot
            import cv2
            plotted_bgr = result.plot()
            _, enc = cv2.imencode(".jpg", plotted_bgr, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
            b64 = "data:image/jpeg;base64," + base64.b64encode(enc).decode("utf-8")

            return {
                "image_width": pil_image.width,
                "image_height": pil_image.height,
                "detections": detections,
                "count": len(detections),
                "inference_ms": elapsed_ms,
                "annotated_image": b64
            }

    # If neither is configured
    raise HTTPException(
        status_code=503,
        detail=(
            "Vercel Serverless functions have a 250MB limit which cannot package the 850MB PyTorch library directly. "
            "To run inference on Vercel, either: (1) Set USE_HUB_API=true and HUB_API_KEY in your Vercel Project Settings, "
            "or (2) Host the backend on Render/Railway/HuggingFace and set REMOTE_BACKEND_URL in Vercel."
        )
    )
