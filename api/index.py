import os
import io
import time
import base64
import logging
from pathlib import Path
from typing import Optional, Dict, Any, List

import httpx
from fastapi import FastAPI, File, UploadFile, Form, HTTPException, status, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from PIL import Image, ImageDraw

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("vercel_api")

app = FastAPI(
    title="AI Object Detection - Ultralytics YOLO",
    description="Vercel Cloud Deployment connected to Ultralytics Cloud Inference API",
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

# Configuration with user's Ultralytics Cloud Run inference endpoint & API key
DEFAULT_HUB_URL = "https://predict-6afebbe7c7fd72b1f958076d-dproatj77a-nw.a.run.app/predict"
DEFAULT_HUB_KEY = "ul_645afcc6c6c448d7046b58259f0cb16c146db9ad"

HUB_MODEL_URL = os.getenv("HUB_MODEL_URL", DEFAULT_HUB_URL)
HUB_API_KEY = os.getenv("HUB_API_KEY", DEFAULT_HUB_KEY)
USE_HUB_API = os.getenv("USE_HUB_API", "true").lower() in ("true", "1", "yes")
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

API_DIR = Path(__file__).resolve().parent
STATIC_DIRS = [
    API_DIR / "static",
    API_DIR,
    API_DIR.parent / "public",
    API_DIR.parent / "public" / "static",
    API_DIR.parent / "webapp" / "static",
    API_DIR.parent,
]

def load_file_content(filename: str) -> Optional[str]:
    """Search multiple candidate locations for static assets."""
    for directory in STATIC_DIRS:
        target = directory / filename
        if target.exists() and target.is_file():
            try:
                return target.read_text(encoding="utf-8")
            except Exception:
                pass
    return None


def draw_bounding_boxes(image_bytes: bytes, detections: List[Dict[str, Any]]) -> str:
    """Draw bounding boxes and class labels directly onto image using PIL."""
    try:
        img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        draw = ImageDraw.Draw(img)

        # Color palette for classes
        colors = ["#10B981", "#4F46E5", "#F59E0B", "#EF4444", "#8B5CF6", "#06B6D4"]

        for idx, det in enumerate(detections):
            bbox = det.get("bbox", [])
            if len(bbox) != 4:
                continue

            x1, y1, x2, y2 = bbox
            color = colors[idx % len(colors)]
            label = f"{det.get('class_name', 'Object')} {det.get('confidence', 0)*100:.1f}%"

            # Draw outer rectangle
            draw.rectangle([x1, y1, x2, y2], outline=color, width=3)

            # Draw text label banner
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


@app.get("/health")
@app.get("/api/health")
def health_check() -> Dict[str, Any]:
    """Health check endpoint for Vercel deployment."""
    return {
        "status": "healthy",
        "platform": "vercel_serverless",
        "model_loaded": True,
        "model_name": "IsaacImage (Ultralytics Cloud Run)",
        "use_hub_api": True,
        "endpoint": HUB_MODEL_URL,
        "classes_count": 1,
        "message": "Connected to Ultralytics Cloud Inference endpoint."
    }


@app.post("/predict")
@app.post("/api/predict")
async def predict(
    file: UploadFile = File(..., description="Image file (JPEG, PNG, or WebP)"),
    conf: float = Form(0.25, description="Confidence threshold between 0.05 and 0.95")
):
    """Run prediction via Ultralytics Cloud Run endpoint."""
    try:
        # 1. Validate file format
        allowed_extensions = {".jpg", ".jpeg", ".png", ".webp"}
        file_ext = Path(file.filename or "").suffix.lower()
        content_type = (file.content_type or "").lower()

        if file_ext not in allowed_extensions and not content_type.startswith("image/"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid file type. Please upload a valid image (JPEG, PNG, or WebP)."
            )

        # 2. Validate file size
        contents = await file.read()
        if len(contents) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"File size exceeds 10 MB limit ({len(contents) / (1024*1024):.2f} MB received)."
            )

        if len(contents) == 0:
            raise HTTPException(status_code=400, detail="Uploaded file is empty.")

        conf_clamped = max(0.05, min(0.95, float(conf)))

        # 3. Get image dimensions
        try:
            pil_img = Image.open(io.BytesIO(contents))
            img_width, img_height = pil_img.size
        except Exception:
            img_width, img_height = 0, 0

        # 4. Call Ultralytics Inference API
        headers = {
            "x-api-key": HUB_API_KEY,
            "Authorization": f"Bearer {HUB_API_KEY}"
        }
        files = {"file": (file.filename or "image.jpg", contents, content_type or "image/jpeg")}
        data = {"conf": str(conf_clamped)}

        start_time = time.perf_counter()
        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                resp = await client.post(HUB_MODEL_URL, headers=headers, files=files, data=data)
                resp.raise_for_status()
                hub_json = resp.json()
            except httpx.HTTPStatusError as e:
                logger.error(f"Ultralytics Cloud API error: {e.response.text}")
                raise HTTPException(
                    status_code=e.response.status_code,
                    detail=f"Ultralytics Cloud API error: {e.response.text}"
                )
            except Exception as e:
                logger.error(f"Connection error to Cloud Run: {e}")
                raise HTTPException(
                    status_code=status.HTTP_502_BAD_GATEWAY,
                    detail=f"Failed to communicate with Ultralytics Cloud Run: {str(e)}"
                )

        inference_ms = round((time.perf_counter() - start_time) * 1000, 2)

        # 5. Parse detections from Ultralytics Cloud Run schema
        detections: List[Dict[str, Any]] = []
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

                class_name = item.get("name") or str(item.get("class", "object"))
                confidence_score = round(float(item.get("confidence", 0)), 4)

                # Filter by confidence threshold
                if confidence_score >= conf_clamped:
                    detections.append({
                        "class_name": class_name,
                        "confidence": confidence_score,
                        "bbox": [x1, y1, x2, y2]
                    })

        # 6. Render annotated image with bounding boxes
        annotated_b64 = draw_bounding_boxes(contents, detections)

        return {
            "image_width": img_width,
            "image_height": img_height,
            "detections": detections,
            "count": len(detections),
            "inference_ms": inference_ms,
            "annotated_image": annotated_b64
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Unexpected error in /predict")
        return JSONResponse(
            status_code=500,
            content={"detail": f"Inference processing error: {str(e)}"}
        )


# Mount static files directory if available
_static_folder = API_DIR / "static"
if _static_folder.exists():
    app.mount("/static", StaticFiles(directory=str(_static_folder)), name="static")


@app.get("/", response_class=HTMLResponse)
@app.get("/index.html", response_class=HTMLResponse)
def serve_index():
    content = load_file_content("index.html")
    if content:
        return HTMLResponse(content=content)
    return HTMLResponse(
        content="""<!DOCTYPE html><html><body><h2>AI Object Detection Webapp</h2><p>Loading UI...</p></body></html>""",
        status_code=200
    )


@app.get("/style.css")
@app.get("/static/style.css")
def serve_css():
    content = load_file_content("style.css")
    if content:
        return Response(content=content, media_type="text/css")
    raise HTTPException(status_code=404, detail="style.css not found")


@app.get("/app.js")
@app.get("/static/app.js")
def serve_js():
    content = load_file_content("app.js")
    if content:
        return Response(content=content, media_type="application/javascript")
    raise HTTPException(status_code=404, detail="app.js not found")
