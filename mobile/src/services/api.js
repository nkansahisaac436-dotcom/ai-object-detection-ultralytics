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
 * Upload image and run YOLO detection via JSON base64.
 * Completely eliminates React Native iOS "Unsupported FormDataPart implementation" errors.
 * 
 * @param {string} imageUri Local URI of image from camera or gallery
 * @param {number} confidence Confidence threshold between 0.05 and 0.95
 * @param {string|null} base64Data Optional pre-read base64 string from ImagePicker
 * @param {string|null} customUrl Optional custom API base URL
 */
export async function runYoloDetection(imageUri, confidence = 0.25, base64Data = null, customUrl = null) {
  const baseUrl = customUrl || CONFIG.API_BASE_URL;
  const endpoint = `${baseUrl}${CONFIG.ENDPOINTS.PREDICT}`;

  try {
    let base64 = base64Data;

    // If base64 wasn't provided directly by image picker, read it from disk
    if (!base64 && imageUri) {
      try {
        const FileSystem = await import("expo-file-system/legacy");
        base64 = await FileSystem.readAsStringAsync(imageUri, {
          encoding: "base64"
        });
      } catch (readErr) {
        console.warn("Could not read file via FileSystem:", readErr);
      }
    }

    if (!base64) {
      throw new Error("Unable to read image data. Please select another photo.");
    }

    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 60000); // 60s timeout for remote cloud inference

    const response = await fetch(endpoint, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Accept": "application/json"
      },
      body: JSON.stringify({
        image: base64,
        conf: confidence
      }),
      signal: controller.signal
    });
    clearTimeout(timeoutId);

    let data;
    const contentType = response.headers.get("content-type") || "";
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
      error: error.name === "AbortError" ? "Detection request timed out. Please try again." : error.message
    };
  }
}
