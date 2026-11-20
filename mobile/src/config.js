// Configuration for Isaac YOLO Detection Mobile App (iOS & Android)

export const CONFIG = {
  // Live Vercel Serverless Production API
  API_BASE_URL: "https://ai-object-detection-ultralytics.vercel.app",

  // Endpoints
  ENDPOINTS: {
    HEALTH: "/health",
    PREDICT: "/predict"
  },

  // Detection parameters
  DEFAULT_CONFIDENCE: 0.25,
  MIN_CONFIDENCE: 0.05,
  MAX_CONFIDENCE: 0.95,

  // App Metadata
  APP_NAME: "Isaac YOLO Detection",
  VERSION: "1.0.0",
  INSTITUTION: "Pentecost University College",
  COURSE: "Artificial Intelligence"
};
