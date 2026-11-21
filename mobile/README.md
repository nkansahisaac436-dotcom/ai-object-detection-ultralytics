# 📱 Isaac YOLO Object Detection Mobile App (iOS & Android)

A cross-platform React Native & Expo mobile application for real-time personal recognition and object detection using custom-trained **Ultralytics YOLO** models.

Designed for the **Artificial Intelligence** coursework at **Pentecost University College**.

---

## 🌟 Key Features
- **Cross-Platform:** Runs identically on **Android** and **iOS** devices.
- **Direct Camera Capture:** Snap photos directly using your phone's camera (`expo-image-picker`).
- **Photo Library Upload:** Select existing photos from your gallery.
- **Live Health Status:** Automatically checks backend connectivity and model readiness (`https://ai-object-detection-ultralytics.vercel.app/health`).
- **Interactive Confidence Slider:** Adjust detection threshold smoothly from 5% to 95%.
- **Dual Visual Modes:** Switch between the original photo and the YOLO annotated output with color-coded bounding boxes.
- **Detailed Detections Breakdown:** Displays identified classes (e.g. *Isaac*), detection confidence %, inference speed (ms), and bounding box coordinates `[x1, y1, x2, y2]`.
- **One-Click Share:** Export or share the annotated detection photo directly to WhatsApp, email, or save to your camera roll (`expo-sharing`).

---

## 🚀 Quick Start Guide (Run on Your Physical Phone)

You do **NOT** need Android Studio or Xcode to test this app on your phone!

### Step 1: Install Expo Go on Your Phone
- **Android:** Download [Expo Go on Google Play Store](https://play.google.com/store/apps/details?id=host.exp.exponent)
- **iPhone (iOS):** Download [Expo Go on Apple App Store](https://apps.apple.com/app/expo-go/id982107779)

### Step 2: Open Terminal on Your PC
Navigate into the `mobile` directory:
```bash
cd mobile
```

### Step 3: Install Dependencies
```bash
npm install
```

### Step 4: Start the Expo Development Server
```bash
npm start
```
or:
```bash
npx expo start
```

### Step 5: Scan the QR Code
- **On Android:** Open the **Expo Go** app and tap **"Scan QR code"**, then scan the QR code displayed in your PC terminal.
- **On iPhone:** Open the default **Camera** app, point it at the QR code on your PC screen, and tap the **"Open in Expo Go"** banner.

The app will load on your physical phone in seconds!

---

## ☁️ Run Anywhere Without Being Close to PC (EAS Cloud Updates)

You can publish this project to your Expo account (`@heaven_bound`) so it appears directly under your **Projects** tab in the Expo Go app on your phone:

```bash
cd mobile
npx eas-cli update --auto
```
Once published, simply open the **Expo Go** app on your phone, navigate to your **Projects** screen under `@heaven_bound`, and tap **`ai-object-detection-mobile`** to run it from anywhere in the world!

---

## 📁 Mobile Directory Structure
```
mobile/
├── App.js                       # Main application view & navigation
├── app.json                     # Expo mobile app configuration & permissions
├── package.json                 # React Native & Expo dependencies
├── babel.config.js              # Babel configuration
├── README.md                    # Mobile user guide & instructions
└── src/
    ├── config.js                # API URLs & detection constants
    ├── services/
    │   └── api.js               # Multi-part upload & health check service
    ├── styles/
    │   └── theme.js             # Modern dark slate/indigo UI theme tokens
    └── components/
        ├── Header.js            # App header with live status badge
        ├── ConfidenceSlider.js  # Interactive confidence slider
        ├── ImagePreview.js      # Dual-tab original/annotated image viewer
        └── DetectionsList.js    # Metric chips & bounding box breakdown
```

---

## ⚙️ Backend Connection
By default, the mobile app connects to the live production serverless API hosted on Vercel:
- **Base URL:** `https://ai-object-detection-ultralytics.vercel.app`
- **Predict Endpoint:** `/predict`
- **Health Endpoint:** `/health`

To point the app to a local development server on your PC, change `API_BASE_URL` in `src/config.js` to your computer's local IP address (e.g. `http://192.168.1.50:8000`).
