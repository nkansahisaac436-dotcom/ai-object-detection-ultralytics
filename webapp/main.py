import os
import io
import time
import base64
import logging
import tempfile
from pathlib import Path
from typing import Optional, Dict, Any, List

from fastapi import FastAPI, File, UploadFile, Form, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from PIL import Image, ImageDraw
import numpy as np
import cv2
import httpx

# Set Ultralytics config dir to temporary folder to avoid permission warnings on Windows
os.environ.setdefault("YOLO_CONFIG_DIR", str(Path(tempfile.gettempdir()) / "Ultralytics"))

# Optional dotenv loading if installed
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("yolo_webapp")

# Directory paths
BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
DEFAULT_MODEL_PATH = BASE_DIR / "model" / "best.pt"
FALLBACK_MODEL_PATH = BASE_DIR / "model" / "yolov8n.pt"

# Ultralytics Cloud Run API Defaults
DEFAULT_HUB_URL = "https://predict-6afebbe7c7fd72b1f958076d-dproatj77a-nw.a.run.app/predict"
DEFAULT_HUB_KEY = "ul_645afcc6c6c448d7046b58259f0cb16c146db9ad"

HUB_MODEL_URL = os.getenv("HUB_MODEL_URL", DEFAULT_HUB_URL)
HUB_API_KEY = os.getenv("HUB_API_KEY", DEFAULT_HUB_KEY)
# If custom best.pt does not exist locally, default to using user's Ultralytics Cloud Run endpoint
USE_HUB_API = os.getenv("USE_HUB_API", "false" if DEFAULT_MODEL_PATH.exists() else "true").lower() in ("true", "1", "yes")

MODEL_PATH = Path(os.getenv("MODEL_PATH", str(DEFAULT_MODEL_PATH)))
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

# FastAPI app
app = FastAPI(
    title="AI Object Detection - Ultralytics YOLO",
    description="Web application for custom Ultralytics YOLO object detection and personal recognition",
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

# Global model state
yolo_model = None
model_loaded = False
active_model_path: Optional[Path] = None
is_starter_model = False
class_names: Dict[int, str] = {}
model_load_error: Optional[str] = None


def draw_bounding_boxes(image_bytes: bytes, detections: List[Dict[str, Any]]) -> str:
    """Draw bounding boxes and class labels directly onto image using PIL."""
    try:
        img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        draw = ImageDraw.Draw(img)
        colors = ["#10B981", "#4F46E5", "#F59E0B", "#EF4444", "#8B5CF6", "#06B6D4"]

        for idx, det in enumerate(detections):
            bbox = det.get("bbox", [])
            if len(bbox) != 4:
                continue

            x1, y1, x2, y2 = bbox
            color = colors[idx % len(colors)]
            label = f"{det.get('class_name', 'Object')} {det.get('confidence', 0)*100:.1f}%"

            draw.rectangle([x1, y1, x2, y2], outline=color, width=3)
            text_pos = (x1, max(0, y1 - 18))
            text_bbox = draw.textbbox(text_pos, label)
            draw.rectangle([text_bbox[0] - 2, text_bbox[1] - 2, text_bbox[2] + 4, text_bbox[3] + 2], fill=color)
            draw.text(text_pos, label, fill="#FFFFFF")

        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=90)
        return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode("utf-8")
    except Exception as e:
        logger.error(f"Error drawing annotations: {e}")
        return "data:image/jpeg;base64," + base64.b64encode(image_bytes).decode("utf-8")


def load_model_at_startup():
    """Load the YOLO model weights once at startup."""
    global yolo_model, model_loaded, class_names, model_load_error, active_model_path, is_starter_model

    if USE_HUB_API:
        logger.info(f"Using Ultralytics Cloud Run Inference API ({HUB_MODEL_URL})")
        model_loaded = True
        active_model_path = None
        is_starter_model = False
        class_names = {0: "Isaac"}
        return

    # Check for target model weights
    target_path = MODEL_PATH
    is_starter = False

    if not target_path.exists():
        if FALLBACK_MODEL_PATH.exists():
            logger.info(f"Custom weights not found at '{target_path}'. Using starter model from '{FALLBACK_MODEL_PATH}'.")
            target_path = FALLBACK_MODEL_PATH
            is_starter = True
        else:
            msg = f"Weights file not found at '{MODEL_PATH}'."
            logger.warning(msg)
            yolo_model = None
            model_loaded = False
            active_model_path = None
            is_starter_model = False
            class_names = {}
            model_load_error = msg
            return

    try:
        from ultralytics import YOLO
        logger.info(f"Loading YOLO model from: {target_path} ...")
        t0 = time.perf_counter()
        yolo_model = YOLO(str(target_path))
        load_time = (time.perf_counter() - t0) * 1000
        model_loaded = True
        active_model_path = target_path
        is_starter_model = is_starter
        class_names = getattr(yolo_model, "names", {})
        model_load_error = None
        logger.info(f"Model loaded successfully in {load_time:.1f}ms! Detected classes: {len(class_names)}")
    except Exception as e:
        model_loaded = False
        yolo_model = None
        active_model_path = None
        is_starter_model = False
        class_names = {}
        model_load_error = str(e)
        logger.error(f"Failed to load YOLO model: {e}", exc_info=True)


# Run model loading
load_model_at_startup()


@app.get("/health")
def health_check() -> Dict[str, Any]:
    """Health check endpoint reporting model status and classes."""
    global model_loaded, is_starter_model
    if (not model_loaded or is_starter_model) and DEFAULT_MODEL_PATH.exists():
        load_model_at_startup()

    message = "Model is loaded and ready for predictions."
    if USE_HUB_API:
        message = "Connected to live Ultralytics Cloud Inference API (IsaacImage model)."
    elif is_starter_model:
        message = "Running with starter model (yolov8n.pt). To use custom model, drop best.pt into webapp/model/."

    return {
        "status": "healthy" if (model_loaded or USE_HUB_API) else "model_not_loaded",
        "model_loaded": model_loaded,
        "is_starter_model": is_starter_model,
        "model_path": str(active_model_path or HUB_MODEL_URL),
        "use_hub_api": USE_HUB_API,
        "class_names": class_names,
        "classes_count": len(class_names),
        "message": message
    }


@app.post("/predict")
async def predict_image(
    file: UploadFile = File(..., description="Image file (JPEG, PNG, or WebP)"),
    conf: float = Form(0.25, description="Confidence threshold between 0.05 and 0.95")
):
    """Predict objects in an uploaded image."""
    # 1. Validate file extension & mime type
    allowed_extensions = {".jpg", ".jpeg", ".png", ".webp"}
    file_ext = Path(file.filename or "").suffix.lower()
    content_type = (file.content_type or "").lower()

    if file_ext not in allowed_extensions and not content_type.startswith("image/"):
        logger.warning(f"Rejected invalid file upload: filename='{file.filename}', content_type='{content_type}'")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file type. Please upload a valid image file (JPEG, PNG, or WebP)."
        )

    # 2. Validate file size (max 10 MB)
    contents = await file.read()
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File size exceeds the 10 MB limit ({len(contents) / (1024*1024):.2f} MB received)."
        )

    if len(contents) == 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Uploaded file is empty.")

    conf_clamped = max(0.05, min(0.95, float(conf)))

    # 3. Check Hub API switch
    if USE_HUB_API:
        return await predict_with_hub_api(contents, conf_clamped, file.filename or "image.jpg")

    # Local model check
    if (not model_loaded or is_starter_model) and DEFAULT_MODEL_PATH.exists():
        load_model_at_startup()

    if not model_loaded or yolo_model is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Model weights not loaded. Please copy your trained 'best.pt' file into webapp/model/."
        )

    # 4. Decode image
    try:
        pil_image = Image.open(io.BytesIO(contents)).convert("RGB")
        width, height = pil_image.size
    except Exception as e:
        raise HTTPException(status_code=400, detail="Could not decode the uploaded image.")

    # 5. Local inference
    start_time = time.perf_counter()
    try:
        results = yolo_model.predict(source=pil_image, conf=conf_clamped, verbose=False)
    except Exception as e:
        logger.error(f"Inference error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Inference failed: {str(e)}")
    inference_ms = round((time.perf_counter() - start_time) * 1000, 2)

    result = results[0]
    detections: List[Dict[str, Any]] = []

    if result.boxes is not None and len(result.boxes) > 0:
        names_dict = result.names or {}
        for box in result.boxes:
            cls_id = int(box.cls[0].item())
            class_name = names_dict.get(cls_id, f"Class {cls_id}")
            confidence_score = round(float(box.conf[0].item()), 4)
            bbox_coords = [round(float(c), 1) for c in box.xyxy[0].tolist()]

            detections.append({
                "class_name": class_name,
                "confidence": confidence_score,
                "bbox": bbox_coords
            })

    # Render annotated image
    try:
        plotted_bgr = result.plot()
        success, encoded_jpg = cv2.imencode(".jpg", plotted_bgr, [int(cv2.IMWRITE_JPEG_QUALITY), 92])
        if not success:
            raise ValueError("Failed to encode")
        annotated_b64 = "data:image/jpeg;base64," + base64.b64encode(encoded_jpg).decode("utf-8")
    except Exception:
        annotated_b64 = draw_bounding_boxes(contents, detections)

    return {
        "image_width": width,
        "image_height": height,
        "detections": detections,
        "count": len(detections),
        "inference_ms": inference_ms,
        "annotated_image": annotated_b64
    }


async def predict_with_hub_api(contents: bytes, conf: float, filename: str) -> Dict[str, Any]:
    """Forward image to user's Ultralytics Cloud Run inference endpoint."""
    headers = {
        "x-api-key": HUB_API_KEY,
        "Authorization": f"Bearer {HUB_API_KEY}"
    }
    files = {"file": (filename, contents, "image/jpeg")}
    data = {"conf": str(conf)}

    try:
        pil_img = Image.open(io.BytesIO(contents))
        img_width, img_height = pil_img.size
    except Exception:
        img_width, img_height = 0, 0

    start_time = time.perf_counter()
    async with httpx.AsyncClient(timeout=40.0) as client:
        try:
            resp = await client.post(HUB_MODEL_URL, headers=headers, files=files, data=data)
            resp.raise_for_status()
            hub_json = resp.json()
        except Exception as e:
            logger.error(f"Ultralytics Cloud Run error: {e}")
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"Ultralytics Cloud inference error: {str(e)}"
            )

    inference_ms = round((time.perf_counter() - start_time) * 1000, 2)

    detections = []
    images_list = hub_json.get("images", [])
    if images_list and len(images_list) > 0:
        first_img = images_list[0]
        results_list = first_img.get("results", [])
        for item in results_list:
            box_dict = item.get("box", {})
            x1 = round(float(box_dict.get("x1", 0)), 1)
            y1 = round(float(box_dict.get("y1", 0)), 1)
            x2 = round(float(box_dict.get("x2", 0)), 1)
            y2 = round(float(box_dict.get("y2", 0)), 1)

            class_name = item.get("name") or str(item.get("class", "Isaac"))
            confidence_score = round(float(item.get("confidence", 0)), 4)

            if confidence_score >= conf:
                detections.append({
                    "class_name": class_name,
                    "confidence": confidence_score,
                    "bbox": [x1, y1, x2, y2]
                })

    annotated_b64 = draw_bounding_boxes(contents, detections)

    return {
        "image_width": img_width,
        "image_height": img_height,
        "detections": detections,
        "count": len(detections),
        "inference_ms": inference_ms,
        "annotated_image": annotated_b64
    }


# Mount static directory
if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


@app.get("/")
def serve_index():
    index_file = STATIC_DIR / "index.html"
    if index_file.exists():
        return FileResponse(index_file)
    return JSONResponse(status_code=404, content={"error": "index.html not found"})


if __name__ == "__main__":
    import uvicorn
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    logger.info(f"Starting server on http://{host}:{port}")
    uvicorn.run("main:app", host=host, port=port, reload=True)
