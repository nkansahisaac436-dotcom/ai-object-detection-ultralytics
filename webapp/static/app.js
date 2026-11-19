// AI Object Detection - Ultralytics Webapp Client
document.addEventListener("DOMContentLoaded", () => {
  // Elements - Tabs & Views
  const tabUpload = document.getElementById("tab-upload");
  const tabWebcam = document.getElementById("tab-webcam");
  const viewUpload = document.getElementById("view-upload");
  const viewWebcam = document.getElementById("view-webcam");

  // Elements - Upload
  const dropZone = document.getElementById("drop-zone");
  const fileInput = document.getElementById("file-input");
  const selectedFileInfo = document.getElementById("selected-file-info");
  const fileNameDisplay = document.getElementById("file-name-display");
  const btnClearFile = document.getElementById("btn-clear-file");

  // Elements - Webcam
  const webcamVideo = document.getElementById("webcam-video");
  const webcamCanvas = document.getElementById("webcam-canvas");
  const webcamPlaceholder = document.getElementById("webcam-placeholder");
  const webcamActions = document.getElementById("webcam-actions");
  const btnStartWebcam = document.getElementById("btn-start-webcam");
  const btnStopWebcam = document.getElementById("btn-stop-webcam");
  const btnCapturePredict = document.getElementById("btn-capture-predict");

  // Elements - Controls
  const confSlider = document.getElementById("conf-slider");
  const confVal = document.getElementById("conf-val");
  const btnPredict = document.getElementById("btn-predict");
  const btnText = document.getElementById("btn-text");
  const btnSpinner = document.getElementById("btn-spinner");

  // Elements - Results & Previews
  const imgOriginal = document.getElementById("img-original");
  const origPlaceholder = document.getElementById("orig-placeholder");
  const imgAnnotated = document.getElementById("img-annotated");
  const annPlaceholder = document.getElementById("ann-placeholder");
  const btnDownload = document.getElementById("btn-download");

  // Elements - Metrics & Table
  const metricCount = document.getElementById("metric-count");
  const metricTime = document.getElementById("metric-time");
  const metricDim = document.getElementById("metric-dim");
  const metricConf = document.getElementById("metric-conf");
  const detectionsTbody = document.getElementById("detections-tbody");

  // Elements - System & Banners
  const systemStatusBadge = document.getElementById("system-status-badge");
  const statusText = document.getElementById("status-text");
  const globalBanner = document.getElementById("global-banner");
  const bannerMessage = document.getElementById("banner-message");
  const bannerClose = document.getElementById("banner-close");

  // State
  let currentFile = null;
  let webcamStream = null;
  let annotatedImageB64 = null;
  let modelAvailable = false;

  // 1. Initial Health Check
  async function checkHealth() {
    try {
      const resp = await fetch("/health");
      if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
      const data = await resp.json();

      if (data.model_loaded || data.use_hub_api) {
        modelAvailable = true;
        systemStatusBadge.className = "status-badge status-online";
        const classCount = data.classes_count || Object.keys(data.class_names || {}).length;
        statusText.textContent = `Model Ready (${classCount} classes)`;
        hideBanner();
      } else {
        modelAvailable = false;
        systemStatusBadge.className = "status-badge status-warning";
        statusText.textContent = "Model Missing";
        showBanner(
          `⚠️ Model weights not found at '${data.model_path}'. Please copy your trained 'best.pt' file into 'webapp/model/' to run predictions.`,
          "warning"
        );
      }
    } catch (err) {
      modelAvailable = false;
      systemStatusBadge.className = "status-badge status-error";
      statusText.textContent = "Server Offline";
      showBanner("⚠️ Cannot connect to backend server. Make sure FastAPI is running (uvicorn main:app).", "danger");
    }
  }

  function showBanner(msg, type = "warning") {
    bannerMessage.innerHTML = msg;
    globalBanner.className = `banner ${type === "danger" ? "banner-danger" : ""}`;
  }

  function hideBanner() {
    globalBanner.className = "banner hidden";
  }

  bannerClose.addEventListener("click", hideBanner);

  // 2. Tab Navigation
  tabUpload.addEventListener("click", () => switchTab("upload"));
  tabWebcam.addEventListener("click", () => switchTab("webcam"));

  function switchTab(mode) {
    if (mode === "upload") {
      tabUpload.classList.add("active");
      tabWebcam.classList.remove("active");
      viewUpload.classList.add("active");
      viewWebcam.classList.remove("active");
    } else {
      tabWebcam.classList.add("active");
      tabUpload.classList.remove("active");
      viewWebcam.classList.add("active");
      viewUpload.classList.remove("active");
      if (!webcamStream) startWebcam();
    }
  }

  // 3. File Upload & Drag-and-Drop
  dropZone.addEventListener("click", () => fileInput.click());

  dropZone.addEventListener("dragover", (e) => {
    e.preventDefault();
    dropZone.classList.add("dragover");
  });

  dropZone.addEventListener("dragleave", () => {
    dropZone.classList.remove("dragover");
  });

  dropZone.addEventListener("drop", (e) => {
    e.preventDefault();
    dropZone.classList.remove("dragover");
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      handleSelectedFile(e.dataTransfer.files[0]);
    }
  });

  fileInput.addEventListener("change", (e) => {
    if (e.target.files && e.target.files.length > 0) {
      handleSelectedFile(e.target.files[0]);
    }
  });

  function handleSelectedFile(file) {
    // Validate file type
    const validTypes = ["image/jpeg", "image/png", "image/webp"];
    if (!validTypes.includes(file.type) && !/\.(jpe?g|png|webp)$/i.test(file.name)) {
      showBanner("Invalid file type. Please select a JPG, PNG, or WebP image.", "danger");
      return;
    }

    // Validate size (10 MB max)
    if (file.size > 10 * 1024 * 1024) {
      showBanner(`File is too large (${(file.size / (1024 * 1024)).toFixed(1)} MB). Maximum allowed size is 10 MB.`, "danger");
      return;
    }

    currentFile = file;
    fileNameDisplay.textContent = `${file.name} (${(file.size / 1024).toFixed(0)} KB)`;
    selectedFileInfo.classList.remove("hidden");
    dropZone.classList.add("hidden");
    btnPredict.disabled = false;

    // Preview original image
    const reader = new FileReader();
    reader.onload = (evt) => {
      imgOriginal.src = evt.target.result;
      imgOriginal.classList.remove("hidden");
      origPlaceholder.classList.add("hidden");
    };
    reader.readAsDataURL(file);

    // Reset previous annotated results
    resetOutputResults();
  }

  btnClearFile.addEventListener("click", () => {
    currentFile = null;
    fileInput.value = "";
    selectedFileInfo.classList.add("hidden");
    dropZone.classList.remove("hidden");
    btnPredict.disabled = true;
    imgOriginal.src = "";
    imgOriginal.classList.add("hidden");
    origPlaceholder.classList.remove("hidden");
    resetOutputResults();
  });

  // 4. Webcam Support
  btnStartWebcam.addEventListener("click", startWebcam);
  btnStopWebcam.addEventListener("click", stopWebcam);

  async function startWebcam() {
    try {
      webcamStream = await navigator.mediaDevices.getUserMedia({
        video: { width: { ideal: 1280 }, height: { ideal: 720 }, facingMode: "user" }
      });
      webcamVideo.srcObject = webcamStream;
      webcamVideo.classList.remove("hidden");
      webcamPlaceholder.classList.add("hidden");
      webcamActions.classList.remove("hidden");
    } catch (err) {
      console.error("Webcam error:", err);
      showBanner(`Could not access webcam: ${err.message}. Please check browser camera permissions.`, "danger");
    }
  }

  function stopWebcam() {
    if (webcamStream) {
      webcamStream.getTracks().forEach((track) => track.stop());
      webcamStream = null;
    }
    webcamVideo.srcObject = null;
    webcamVideo.classList.add("hidden");
    webcamPlaceholder.classList.remove("hidden");
    webcamActions.classList.add("hidden");
  }

  btnCapturePredict.addEventListener("click", () => {
    if (!webcamVideo || !webcamStream) return;

    webcamCanvas.width = webcamVideo.videoWidth || 640;
    webcamCanvas.height = webcamVideo.videoHeight || 480;
    const ctx = webcamCanvas.getContext("2d");
    ctx.drawImage(webcamVideo, 0, 0, webcamCanvas.width, webcamCanvas.height);

    // Convert canvas to blob
    webcamCanvas.toBlob(
      (blob) => {
        if (!blob) return;
        const webcamFile = new File([blob], "webcam_capture.jpg", { type: "image/jpeg" });
        currentFile = webcamFile;

        // Set original preview
        imgOriginal.src = webcamCanvas.toDataURL("image/jpeg");
        imgOriginal.classList.remove("hidden");
        origPlaceholder.classList.add("hidden");

        // Run prediction immediately
        runPrediction();
      },
      "image/jpeg",
      0.95
    );
  });

  // 5. Confidence Slider
  confSlider.addEventListener("input", (e) => {
    const val = parseFloat(e.target.value);
    const pct = Math.round(val * 100);
    confVal.textContent = `${pct}% (${val.toFixed(2)})`;
    metricConf.textContent = val.toFixed(2);
  });

  // 6. Predict Action
  btnPredict.addEventListener("click", runPrediction);

  async function runPrediction() {
    if (!currentFile) {
      showBanner("Please select or capture an image first.", "warning");
      return;
    }

    setLoading(true);
    hideBanner();

    const formData = new FormData();
    formData.append("file", currentFile);
    formData.append("conf", confSlider.value);

    try {
      const resp = await fetch("/predict", {
        method: "POST",
        body: formData
      });

      const data = await resp.json();

      if (!resp.ok) {
        const errorMsg = data.detail || `Server returned error status ${resp.status}`;
        showBanner(`⚠️ ${errorMsg}`, "danger");
        return;
      }

      displayResults(data);
    } catch (err) {
      console.error("Predict error:", err);
      showBanner(`⚠️ Network or server error: ${err.message}`, "danger");
    } finally {
      setLoading(false);
    }
  }

  function setLoading(isLoading) {
    if (isLoading) {
      btnPredict.disabled = true;
      btnCapturePredict.disabled = true;
      btnSpinner.classList.remove("hidden");
      btnText.textContent = "Running YOLO Inference...";
    } else {
      btnPredict.disabled = !currentFile;
      btnCapturePredict.disabled = false;
      btnSpinner.classList.add("hidden");
      btnText.textContent = "Run YOLO Detection";
    }
  }

  // 7. Render Prediction Results
  function displayResults(data) {
    // Metrics
    metricCount.textContent = data.count;
    metricTime.textContent = `${data.inference_ms} ms`;
    metricDim.textContent = `${data.image_width} × ${data.image_height}`;
    metricConf.textContent = confSlider.value;

    // Annotated Image Preview
    if (data.annotated_image) {
      annotatedImageB64 = data.annotated_image;
      imgAnnotated.src = data.annotated_image;
      imgAnnotated.classList.remove("hidden");
      annPlaceholder.classList.add("hidden");
      btnDownload.classList.remove("hidden");
    }

    // Populate Detections Table
    detectionsTbody.innerHTML = "";
    if (!data.detections || data.detections.length === 0) {
      const emptyTr = document.createElement("tr");
      emptyTr.className = "empty-row";
      emptyTr.innerHTML = `<td colspan="4">No objects detected above the ${Math.round(confSlider.value * 100)}% threshold.</td>`;
      detectionsTbody.appendChild(emptyTr);
      return;
    }

    data.detections.forEach((det, idx) => {
      const tr = document.createElement("tr");
      const confPct = (det.confidence * 100).toFixed(1);
      const bboxStr = Array.isArray(det.bbox) ? `[${det.bbox.join(", ")}]` : "-";

      tr.innerHTML = `
        <td><strong>#${idx + 1}</strong></td>
        <td><span class="badge-class">${escapeHtml(det.class_name)}</span></td>
        <td><span class="badge-conf">${confPct}%</span></td>
        <td><code class="bbox-coord">${bboxStr}</code></td>
      `;
      detectionsTbody.appendChild(tr);
    });
  }

  function resetOutputResults() {
    annotatedImageB64 = null;
    imgAnnotated.src = "";
    imgAnnotated.classList.add("hidden");
    annPlaceholder.classList.remove("hidden");
    btnDownload.classList.add("hidden");
    metricCount.textContent = "-";
    metricTime.textContent = "-";
    metricDim.textContent = "-";
    detectionsTbody.innerHTML = `
      <tr class="empty-row">
        <td colspan="4">No predictions yet. Click 'Run YOLO Detection' or use webcam.</td>
      </tr>
    `;
  }

  // 8. Download Annotated Result
  btnDownload.addEventListener("click", () => {
    if (!annotatedImageB64) return;
    const link = document.createElement("a");
    const timestamp = new Date().toISOString().replace(/[:.]/g, "-");
    link.download = `yolo_detection_${timestamp}.jpg`;
    link.href = annotatedImageB64;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  });

  function escapeHtml(text) {
    const div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
  }

  // Run initial health check on load
  checkHealth();
});
