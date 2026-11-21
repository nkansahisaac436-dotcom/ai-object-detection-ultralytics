import React, { useState, useEffect } from "react";
import {
  StyleSheet,
  View,
  Text,
  ScrollView,
  TouchableOpacity,
  SafeAreaView,
  Alert,
  RefreshControl
} from "react-native";
import { StatusBar } from "expo-status-bar";
import * as ImagePicker from "expo-image-picker";

import Header from "./src/components/Header";
import ConfidenceSlider from "./src/components/ConfidenceSlider";
import ImagePreview from "./src/components/ImagePreview";
import DetectionsList from "./src/components/DetectionsList";
import { checkServerHealth, runYoloDetection } from "./src/services/api";
import { CONFIG } from "./src/config";
import { COLORS, SPACING, RADIUS } from "./src/styles/theme";

export default function App() {
  // State
  const [serverStatus, setServerStatus] = useState("loading"); // 'loading', 'online', 'offline'
  const [serverMessage, setServerMessage] = useState("Checking Model...");
  const [refreshing, setRefreshing] = useState(false);

  const [selectedImageUri, setSelectedImageUri] = useState(null);
  const [selectedImageBase64, setSelectedImageBase64] = useState(null);
  const [annotatedImageUri, setAnnotatedImageUri] = useState(null);
  const [confidence, setConfidence] = useState(CONFIG.DEFAULT_CONFIDENCE);
  const [loading, setLoading] = useState(false);
  const [detectionResults, setDetectionResults] = useState(null);
  const [bannerError, setBannerError] = useState(null);

  // Initial Health Check
  useEffect(() => {
    performHealthCheck();
  }, []);

  const performHealthCheck = async () => {
    setServerStatus("loading");
    setServerMessage("Connecting...");
    const res = await checkServerHealth();

    if (res.success && res.data.status === "healthy") {
      setServerStatus("online");
      const modelName = res.data.model_name || "YOLO Ready";
      setServerMessage(`Model Ready (${res.data.classes_count || 1} class)`);
      setBannerError(null);
    } else {
      setServerStatus("offline");
      setServerMessage("Server Offline");
      setBannerError(res.error || "Cannot reach YOLO backend API.");
    }
  };

  const onRefresh = async () => {
    setRefreshing(true);
    await performHealthCheck();
    setRefreshing(false);
  };

  // Camera Action
  const handleTakePhoto = async () => {
    setBannerError(null);
    try {
      const permission = await ImagePicker.requestCameraPermissionsAsync();
      if (!permission.granted) {
        Alert.alert(
          "Permission Required",
          "Camera access is needed to capture photos for detection."
        );
        return;
      }

      const result = await ImagePicker.launchCameraAsync({
        mediaTypes: ImagePicker.MediaTypeOptions.Images,
        allowsEditing: false,
        quality: 0.75,
        base64: true
      });

      if (!result.canceled && result.assets && result.assets.length > 0) {
        const asset = result.assets[0];
        setSelectedImageUri(asset.uri);
        setSelectedImageBase64(asset.base64 || null);
        setAnnotatedImageUri(null);
        setDetectionResults(null);
      }
    } catch (err) {
      setBannerError("Failed to open camera: " + err.message);
    }
  };

  // Gallery Action
  const handleChoosePhoto = async () => {
    setBannerError(null);
    try {
      const permission = await ImagePicker.requestMediaLibraryPermissionsAsync();
      if (!permission.granted) {
        Alert.alert(
          "Permission Required",
          "Photo library access is needed to select an image for detection."
        );
        return;
      }

      const result = await ImagePicker.launchImageLibraryAsync({
        mediaTypes: ImagePicker.MediaTypeOptions.Images,
        allowsEditing: false,
        quality: 0.75,
        base64: true
      });

      if (!result.canceled && result.assets && result.assets.length > 0) {
        const asset = result.assets[0];
        setSelectedImageUri(asset.uri);
        setSelectedImageBase64(asset.base64 || null);
        setAnnotatedImageUri(null);
        setDetectionResults(null);
      }
    } catch (err) {
      setBannerError("Failed to open photo library: " + err.message);
    }
  };

  // Run YOLO Inference
  const handleRunDetection = async () => {
    if (!selectedImageUri) {
      Alert.alert("Select Image", "Please take a photo or select one from your gallery first.");
      return;
    }

    setLoading(true);
    setBannerError(null);

    const res = await runYoloDetection(selectedImageUri, confidence, selectedImageBase64);
    setLoading(false);

    if (res.success) {
      setDetectionResults(res.data);
      if (res.data.annotatedImage) {
        setAnnotatedImageUri(res.data.annotatedImage);
      }
    } else {
      setBannerError(res.error || "Failed to execute YOLO detection.");
    }
  };

  const handleClear = () => {
    setSelectedImageUri(null);
    setSelectedImageBase64(null);
    setAnnotatedImageUri(null);
    setDetectionResults(null);
    setBannerError(null);
  };

  return (
    <SafeAreaView style={styles.safeArea}>
      <StatusBar style="light" />

      {/* Header */}
      <Header status={serverStatus} statusMessage={serverMessage} />

      <ScrollView
        style={styles.container}
        contentContainerStyle={styles.contentContainer}
        refreshControl={
          <RefreshControl
            refreshing={refreshing}
            onRefresh={onRefresh}
            tintColor={COLORS.primaryLight}
          />
        }
      >
        {/* Error Banner */}
        {bannerError && (
          <View style={styles.errorBanner}>
            <Text style={styles.errorIcon}>⚠️</Text>
            <Text style={styles.errorText}>{bannerError}</Text>
          </View>
        )}

        {/* Action Buttons: Camera & Gallery */}
        <View style={styles.actionRow}>
          <TouchableOpacity
            style={[styles.btnAction, styles.btnPrimary]}
            onPress={handleTakePhoto}
            disabled={loading}
          >
            <Text style={styles.btnActionIcon}>📷</Text>
            <Text style={styles.btnActionText}>Take Photo</Text>
          </TouchableOpacity>

          <TouchableOpacity
            style={[styles.btnAction, styles.btnSecondary]}
            onPress={handleChoosePhoto}
            disabled={loading}
          >
            <Text style={styles.btnActionIcon}>🖼️</Text>
            <Text style={styles.btnActionText}>Gallery</Text>
          </TouchableOpacity>
        </View>

        {/* Confidence Threshold Slider */}
        <ConfidenceSlider
          confidence={confidence}
          onConfidenceChange={setConfidence}
        />

        {/* Image Preview & Results */}
        <ImagePreview
          originalUri={selectedImageUri}
          annotatedUri={annotatedImageUri}
          loading={loading}
          onClear={handleClear}
        />

        {/* Run Prediction Button */}
        {selectedImageUri && !annotatedImageUri && (
          <TouchableOpacity
            style={[styles.btnPredict, loading && styles.btnPredictDisabled]}
            onPress={handleRunDetection}
            disabled={loading}
          >
            <Text style={styles.btnPredictText}>
              {loading ? "Running YOLO Inference..." : "🎯 Run YOLO Detection"}
            </Text>
          </TouchableOpacity>
        )}

        {/* Detections Breakdown */}
        {detectionResults && <DetectionsList results={detectionResults} />}

        {/* Footer info */}
        <View style={styles.footer}>
          <Text style={styles.footerText}>Pentecost University College • AI Coursework</Text>
          <Text style={styles.footerSubtext}>Ultralytics YOLO Custom Detection • Isaac Recognition</Text>
        </View>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safeArea: {
    flex: 1,
    backgroundColor: COLORS.background,
  },
  container: {
    flex: 1,
    backgroundColor: COLORS.background,
  },
  contentContainer: {
    paddingBottom: SPACING.xl,
  },
  errorBanner: {
    flexDirection: "row",
    alignItems: "center",
    backgroundColor: "rgba(239, 68, 68, 0.15)",
    borderWidth: 1,
    borderColor: COLORS.danger,
    marginHorizontal: SPACING.md,
    marginTop: SPACING.sm,
    padding: SPACING.sm + 2,
    borderRadius: RADIUS.md,
  },
  errorIcon: {
    fontSize: 16,
    marginRight: 8,
  },
  errorText: {
    flex: 1,
    fontSize: 12,
    color: COLORS.danger,
    fontWeight: "500",
  },
  actionRow: {
    flexDirection: "row",
    gap: SPACING.sm,
    marginHorizontal: SPACING.md,
    marginTop: SPACING.md,
    marginBottom: SPACING.xs,
  },
  btnAction: {
    flex: 1,
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "center",
    paddingVertical: SPACING.sm + 4,
    borderRadius: RADIUS.md,
  },
  btnPrimary: {
    backgroundColor: COLORS.primary,
  },
  btnSecondary: {
    backgroundColor: COLORS.surface,
    borderWidth: 1,
    borderColor: COLORS.border,
  },
  btnActionIcon: {
    fontSize: 18,
    marginRight: 6,
  },
  btnActionText: {
    fontSize: 14,
    fontWeight: "700",
    color: COLORS.text,
  },
  btnPredict: {
    backgroundColor: COLORS.accent,
    marginHorizontal: SPACING.md,
    marginVertical: SPACING.sm,
    paddingVertical: SPACING.md,
    borderRadius: RADIUS.md,
    alignItems: "center",
  },
  btnPredictDisabled: {
    opacity: 0.6,
  },
  btnPredictText: {
    fontSize: 15,
    fontWeight: "700",
    color: "#0F172A",
  },
  footer: {
    alignItems: "center",
    marginTop: SPACING.lg,
    paddingVertical: SPACING.md,
  },
  footerText: {
    fontSize: 11,
    fontWeight: "600",
    color: COLORS.textMuted,
  },
  footerSubtext: {
    fontSize: 10,
    color: COLORS.textMuted,
    marginTop: 2,
  },
});
