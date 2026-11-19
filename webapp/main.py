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
from PIL import Image
import numpy as np
import cv2

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

# Environment variables
MODEL_PATH = Path(os.getenv("MODEL_PATH", str(DEFAULT_MODEL_PATH)))
USE_HUB_API = os.getenv("USE_HUB_API", "false").lower() in ("true", "1", "yes")
HUB_API_KEY = os.getenv("HUB_API_KEY", "")
HUB_MODEL_URL = os.getenv("HUB_MODEL_URL", "https://api.ultralytics.com/v1/predict")
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


def load_model_at_startup():
    """Load the YOLO model weights once at startup."""
    global yolo_model, model_loaded, class_names, model_load_error, active_model_path, is_starter_model

    if USE_HUB_API:
        logger.info("Configured to use Ultralytics HUB API (USE_HUB_API=true).")
        model_loaded = True
        active_model_path = None
        is_starter_model = False
        class_names = {0: "hub_model_detection"}
        return

    # Check for target model weights
    target_path = MODEL_PATH
    is_starter = False

    if not target_path.exists():
        # Check if fallback demo model exists
        if FALLBACK_MODEL_PATH.exists():
            logger.info(
                f"Custom weights not found at '{target_path}'. "
                f"Loading starter demo model from '{FALLBACK_MODEL_PATH}'."
            )
            target_path = FALLBACK_MODEL_PATH
            is_starter = True
        else:
            msg = (
                f"Weights file not found at '{MODEL_PATH}'. "
                f"Please place your trained 'best.pt' file into '{DEFAULT_MODEL_PATH.parent}' "
                f"or update the MODEL_PATH environment variable."
            )
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
        logger.info(
            f"Model loaded successfully in {load_time:.1f}ms! "
            f"Starter model: {is_starter}. Detected classes count: {len(class_names)}"
        )
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
    # Check if custom best.pt was dropped in since startup
    global model_loaded, is_starter_model
    if (not model_loaded or is_starter_model) and DEFAULT_MODEL_PATH.exists():
        load_model_at_startup()

    message = "Model is loaded and ready for predictions."
    if is_starter_model:
        message = (
            "Running with starter model (yolov8n.pt). "
            "To use your custom model, drop 'best.pt' into 'webapp/model/'."
        )
    elif not model_loaded:
        message = model_load_error or "Model weights not found. Please place best.pt into webapp/model/."

    return {
        "status": "healthy" if (model_loaded or USE_HUB_API) else "model_not_loaded",
        "model_loaded": model_loaded,
        "is_starter_model": is_starter_model,
        "model_path": str(active_model_path or MODEL_PATH),
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
    """
    Predict objects in an uploaded image.
    Returns bounding boxes, labels, confidence scores, count, inference time,
    and base64 encoded annotated image.
    """
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
        logger.warning(f"Rejected file exceeding 10 MB: {len(contents)} bytes")
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File size exceeds the 10 MB limit ({len(contents) / (1024*1024):.2f} MB received)."
        )

    if len(contents) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file is empty."
        )

    # Validate / clamp confidence
    conf_clamped = max(0.05, min(0.95, float(conf)))

    # 3. Check Hub API switch or local model
    if USE_HUB_API:
        if not HUB_API_KEY:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="HUB_API_KEY environment variable is required when USE_HUB_API=true."
            )
        return await predict_with_hub_api(contents, conf_clamped, file.filename or "image.jpg")

    # Local model check: if best.pt was dropped in, hot-reload it
    if (not model_loaded or is_starter_model) and DEFAULT_MODEL_PATH.exists():
        load_model_at_startup()

    if not model_loaded or yolo_model is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=(
                f"Model weights not loaded. Please copy your trained 'best.pt' file into "
                f"'{DEFAULT_MODEL_PATH.parent}' or set the MODEL_PATH environment variable."
            )
        )

    # 4. Decode image
    try:
        pil_image = Image.open(io.BytesIO(contents)).convert("RGB")
        width, height = pil_image.size
    except Exception as e:
        logger.error(f"Corrupted image data: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not decode the uploaded image. Please verify it is a valid image file."
        )

    # 5. Run inference
    start_time = time.perf_counter()
    try:
        results = yolo_model.predict(source=pil_image, conf=conf_clamped, verbose=False)
    except Exception as e:
        logger.error(f"Inference error: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Inference failed: {str(e)}"
        )
    inference_ms = round((time.perf_counter() - start_time) * 1000, 2)

    result = results[0]
    detections: List[Dict[str, Any]] = []

    # 6. Extract detections
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
                "bbox": bbox_coords  # [x1, y1, x2, y2]
            })

    # 7. Render annotated image
    try:
        plotted_bgr = result.plot()
        success, encoded_jpg = cv2.imencode(".jpg", plotted_bgr, [int(cv2.IMWRITE_JPEG_QUALITY), 92])
        if not success:
            raise ValueError("Failed to encode annotated image to JPEG")
        annotated_b64 = "data:image/jpeg;base64," + base64.b64encode(encoded_jpg).decode("utf-8")
    except Exception as e:
        logger.warning(f"Error encoding OpenCV annotated plot: {e}, falling back to PIL")
        plotted_rgb = Image.fromarray(cv2.cvtColor(result.plot(), cv2.COLOR_BGR2RGB))
        buf = io.BytesIO()
        plotted_rgb.save(buf, format="JPEG", quality=90)
        annotated_b64 = "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode("utf-8")

    logger.info(
        f"Prediction complete: {len(detections)} detection(s) found in {inference_ms}ms "
        f"(confidence threshold: {conf_clamped})"
    )

    return {
        "image_width": width,
        "image_height": height,
        "detections": detections,
        "count": len(detections),
        "inference_ms": inference_ms,
        "annotated_image": annotated_b64
    }


async def predict_with_hub_api(contents: bytes, conf: float, filename: str) -> Dict[str, Any]:
    """Forward image to Ultralytics HUB API inference endpoint."""
    import httpx

    headers = {"x-api-key": HUB_API_KEY}
    files = {"file": (filename, contents, "image/jpeg")}
    data = {"conf": str(conf)}

    start_time = time.perf_counter()
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            resp = await client.post(HUB_MODEL_URL, headers=headers, files=files, data=data)
            resp.raise_for_status()
            hub_json = resp.json()
        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code,
                detail=f"Ultralytics HUB API returned error: {e.response.text}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"Failed to communicate with Ultralytics HUB API: {str(e)}"
            )

    inference_ms = round((time.perf_counter() - start_time) * 1000, 2)
    return {
        "image_width": hub_json.get("image_width", 0),
        "image_height": hub_json.get("image_height", 0),
        "detections": hub_json.get("detections", []),
        "count": len(hub_json.get("detections", [])),
        "inference_ms": inference_ms,
        "annotated_image": hub_json.get("annotated_image", "")
    }


# Mount static directory
if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


@app.get("/")
def serve_index():
    """Serve the single-page frontend application."""
    index_file = STATIC_DIR / "index.html"
    if index_file.exists():
        return FileResponse(index_file)
    return JSONResponse(
        status_code=404,
        content={"error": "Frontend static file index.html not found"}
    )


if __name__ == "__main__":
    import uvicorn
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    logger.info(f"Starting server on http://{host}:{port}")
    uvicorn.run("main:app", host=host, port=port, reload=True)
