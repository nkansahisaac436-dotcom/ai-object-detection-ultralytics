import { CONFIG } from "../config";

/**
 * Check backend server and model availability.
 */
export async function checkServerHealth(customUrl = null) {
  const baseUrl = customUrl || CONFIG.API_BASE_URL;
  const endpoint = `${baseUrl}${CONFIG.ENDPOINTS.HEALTH}`;

  try {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 8000);

    const response = await fetch(endpoint, {
      method: "GET",
      signal: controller.signal
    });
    clearTimeout(timeoutId);

    if (!response.ok) {
      throw new Error(`Server returned HTTP ${response.status}`);
    }

    const data = await response.json();
    return {
      success: true,
      data
    };
  } catch (error) {
    return {
      success: false,
      error: error.name === "AbortError" ? "Health check request timed out." : error.message
    };
  }
}

/**
 * Upload image and run YOLO detection via the inference endpoint.
 * @param {string} imageUri Local URI of image from camera or gallery
 * @param {number} confidence Confidence threshold between 0.05 and 0.95
 * @param {string|null} customUrl Optional custom API base URL
 */
export async function runYoloDetection(imageUri, confidence = 0.25, customUrl = null) {
  const baseUrl = customUrl || CONFIG.API_BASE_URL;
  const endpoint = `${baseUrl}${CONFIG.ENDPOINTS.PREDICT}`;

  const formData = new FormData();

  // Extract file name or create default
  const uriParts = imageUri.split("/");
  const fileName = uriParts[uriParts.length - 1] || "capture.jpg";

  // Determine mime type
  let mimeType = "image/jpeg";
  if (fileName.toLowerCase().endsWith(".png")) mimeType = "image/png";
  if (fileName.toLowerCase().endsWith(".webp")) mimeType = "image/webp";

  formData.append("file", {
    uri: imageUri,
    name: fileName,
    type: mimeType
  });
  formData.append("conf", String(confidence));

  try {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 45000); // 45s timeout

    const response = await fetch(endpoint, {
      method: "POST",
      body: formData,
      headers: {
        Accept: "application/json"
      },
      signal: controller.signal
    });
    clearTimeout(timeoutId);

    const contentType = response.headers.get("content-type") || "";
    let data;
    if (contentType.includes("application/json")) {
      data = await response.json();
    } else {
      const text = await response.text();
      data = { detail: text || `Server error (${response.status})` };
    }

    if (!response.ok) {
      throw new Error(data.detail || `Inference failed with status ${response.status}`);
    }

    return {
      success: true,
      data: {
        imageWidth: data.image_width,
        imageHeight: data.image_height,
        detections: data.detections || [],
        count: data.count || 0,
        inferenceMs: data.inference_ms || 0,
        annotatedImage: data.annotated_image // base64 data URI
      }
    };
  } catch (error) {
    return {
      success: false,
      error: error.name === "AbortError" ? "Detection request timed out." : error.message
    };
  }
}
