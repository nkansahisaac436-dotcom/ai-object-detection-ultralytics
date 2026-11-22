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
  const fileThumbImg = document.getElementById("file-thumb-img");
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

  // Elements - History
  const btnToggleHistory = document.getElementById("btn-toggle-history");
  const historyBadge = document.getElementById("history-badge");
  const historyModal = document.getElementById("history-modal");
  const historyList = document.getElementById("history-list");
  const btnCloseHistory = document.getElementById("btn-close-history");
  const btnCloseHistoryFooter = document.getElementById("btn-close-history-footer");
  const btnClearWebHistory = document.getElementById("btn-clear-web-history");

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
  let detectionHistory = [];

  try {
    const saved = localStorage.getItem("isaac_yolo_history");
    if (saved) detectionHistory = JSON.parse(saved);
  } catch (e) {
    detectionHistory = [];
  }
  updateHistoryBadge();

  function updateHistoryBadge() {
    if (historyBadge) historyBadge.textContent = detectionHistory.length;
  }

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
    if (!file) return;

    hideBanner();
    currentFile = file;
    fileNameDisplay.textContent = `${file.name || "photo.jpg"} (${(file.size / 1024).toFixed(0)} KB)`;
    selectedFileInfo.classList.remove("hidden");
    dropZone.classList.add("hidden");
    btnPredict.disabled = false;

    // Use native ObjectURL for instant rendering on mobile
    const objectUrl = URL.createObjectURL(file);
    if (fileThumbImg) {
      fileThumbImg.src = objectUrl;
    }
    imgOriginal.src = objectUrl;
    imgOriginal.classList.remove("hidden");
    origPlaceholder.classList.add("hidden");

    // Convert & optimize to JPEG to support iPhone HEIC and speed up uploads
    const tempImg = new Image();
    tempImg.onload = () => {
      try {
        const maxDim = 960;
        let w = tempImg.naturalWidth || tempImg.width;
        let h = tempImg.naturalHeight || tempImg.height;
        let scale = 1;
        if (w > maxDim || h > maxDim) {
          scale = maxDim / Math.max(w, h);
        }
        const canvas = document.createElement("canvas");
        canvas.width = Math.round(w * scale);
        canvas.height = Math.round(h * scale);
        const ctx = canvas.getContext("2d");
        ctx.drawImage(tempImg, 0, 0, canvas.width, canvas.height);

        const jpegDataUrl = canvas.toDataURL("image/jpeg", 0.80);
        if (fileThumbImg) fileThumbImg.src = jpegDataUrl;
        imgOriginal.src = jpegDataUrl;

        canvas.toBlob((blob) => {
          if (blob) {
            currentFile = blob;
          }
        }, "image/jpeg", 0.80);
      } catch (err) {
        console.warn("Canvas conversion fallback:", err);
      }
    };
    tempImg.onerror = () => {
      const reader = new FileReader();
      reader.onload = (evt) => {
        if (fileThumbImg) fileThumbImg.src = evt.target.result;
        imgOriginal.src = evt.target.result;
      };
      reader.readAsDataURL(file);
    };
    tempImg.src = objectUrl;

    // Reset previous annotated results
    resetOutputResults();
  }

  btnClearFile.addEventListener("click", () => {
    currentFile = null;
    fileInput.value = "";
    if (fileThumbImg) fileThumbImg.src = "";
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
    formData.append("file", currentFile, currentFile.name || "upload.jpg");
    formData.append("conf", confSlider.value);

    try {
      const resp = await fetch("/predict", {
        method: "POST",
        body: formData
      });

      let data;
      const contentType = resp.headers.get("content-type") || "";
      if (contentType.includes("application/json")) {
        data = await resp.json();
      } else {
        const text = await resp.text();
        data = { detail: text || `Server error (${resp.status})` };
      }

      if (!resp.ok) {
        const errorMsg = data.detail || `Server returned error status ${resp.status}`;
        showBanner(`⚠️ ${errorMsg}`, "danger");
        return;
      }

      displayResults(data);
      // On mobile devices, smoothly scroll down to display results
      if (window.innerWidth <= 950) {
        setTimeout(() => {
          document.querySelector(".results-section")?.scrollIntoView({ behavior: "smooth" });
        }, 100);
      }
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

    // Save to History
    try {
      const historyItem = {
        id: Date.now().toString(),
        timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
        originalSrc: imgOriginal.src,
        annotatedSrc: data.annotated_image,
        count: data.count || 0,
        inferenceMs: data.inference_ms || 0,
        imageWidth: data.image_width,
        imageHeight: data.image_height,
        detections: data.detections || [],
        conf: confSlider.value
      };
      detectionHistory.unshift(historyItem);
      if (detectionHistory.length > 25) detectionHistory.pop();
      localStorage.setItem("isaac_yolo_history", JSON.stringify(detectionHistory));
      updateHistoryBadge();
    } catch (err) {
      console.warn("History save note:", err);
    }
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

  // 9. Tested Images History Modal
  if (btnToggleHistory) {
    btnToggleHistory.addEventListener("click", openHistoryModal);
  }
  if (btnCloseHistory) {
    btnCloseHistory.addEventListener("click", closeHistoryModal);
  }
  if (btnCloseHistoryFooter) {
    btnCloseHistoryFooter.addEventListener("click", closeHistoryModal);
  }
  if (btnClearWebHistory) {
    btnClearWebHistory.addEventListener("click", () => {
      if (confirm("Clear all previously tested images?")) {
        detectionHistory = [];
        try { localStorage.removeItem("isaac_yolo_history"); } catch (e) {}
        updateHistoryBadge();
        renderHistoryList();
      }
    });
  }

  function openHistoryModal() {
    renderHistoryList();
    historyModal.classList.remove("hidden");
  }

  function closeHistoryModal() {
    historyModal.classList.add("hidden");
  }

  function renderHistoryList() {
    if (!historyList) return;
    historyList.innerHTML = "";

    if (detectionHistory.length === 0) {
      historyList.innerHTML = `
        <div class="history-empty">
          <div class="history-empty-icon">📷</div>
          <h4>No Tested Images Yet</h4>
          <p>Run YOLO detection on any photo to save and review past results here.</p>
        </div>
      `;
      return;
    }

    detectionHistory.forEach((item, idx) => {
      const card = document.createElement("div");
      card.className = "history-card";
      const countText = item.count > 0 ? `${item.count} Detected` : "0 Found";
      const confPct = Math.round(parseFloat(item.conf || 0.25) * 100);

      card.innerHTML = `
        <div class="history-thumb-wrap">
          <img src="${item.annotatedSrc || item.originalSrc}" class="history-thumb" alt="Tested photo" />
          <span class="history-badge-overlay">${countText}</span>
        </div>
        <div class="history-body">
          <span class="history-time">#${detectionHistory.length - idx} • ${item.timestamp}</span>
          <div class="history-meta">
            <span>Threshold: <strong>${confPct}%</strong></span>
            <span>Speed: <strong>${item.inferenceMs} ms</strong></span>
          </div>
          <div class="history-actions">
            <button class="btn btn-primary btn-sm btn-restore-test">Restore</button>
            <button class="btn btn-secondary btn-sm btn-download-test">Download</button>
          </div>
        </div>
      `;

      // Event listener for Restore
      card.querySelector(".btn-restore-test").addEventListener("click", () => {
        restoreHistoryItem(item);
        closeHistoryModal();
      });

      // Event listener for Download
      card.querySelector(".btn-download-test").addEventListener("click", () => {
        const link = document.createElement("a");
        link.download = `yolo_test_${item.timestamp.replace(/[: ]/g, "_")}.jpg`;
        link.href = item.annotatedSrc || item.originalSrc;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
      });

      historyList.appendChild(card);
    });
  }

  function restoreHistoryItem(item) {
    if (item.originalSrc) {
      imgOriginal.src = item.originalSrc;
      imgOriginal.classList.remove("hidden");
      origPlaceholder.classList.add("hidden");
    }
    if (item.annotatedSrc) {
      annotatedImageB64 = item.annotatedSrc;
      imgAnnotated.src = item.annotatedSrc;
      imgAnnotated.classList.remove("hidden");
      annPlaceholder.classList.add("hidden");
      btnDownload.classList.remove("hidden");
    }
    if (item.conf) {
      confSlider.value = item.conf;
      const pct = Math.round(parseFloat(item.conf) * 100);
      confVal.textContent = `${pct}% (${parseFloat(item.conf).toFixed(2)})`;
      metricConf.textContent = parseFloat(item.conf).toFixed(2);
    }
    metricCount.textContent = item.count;
    metricTime.textContent = `${item.inferenceMs} ms`;
    metricDim.textContent = item.dimensions || "-";

    // Render detections table
    detectionsTbody.innerHTML = "";
    if (!item.detections || item.detections.length === 0) {
      const emptyTr = document.createElement("tr");
      emptyTr.className = "empty-row";
      emptyTr.innerHTML = `<td colspan="4">No objects detected above threshold.</td>`;
      detectionsTbody.appendChild(emptyTr);
    } else {
      item.detections.forEach((det, idx) => {
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

    // Smooth scroll down to results section on mobile
    if (window.innerWidth <= 950) {
      setTimeout(() => {
        document.querySelector(".results-section")?.scrollIntoView({ behavior: "smooth" });
      }, 100);
    }
  }

  // Run initial health check on load
  checkHealth();
});
