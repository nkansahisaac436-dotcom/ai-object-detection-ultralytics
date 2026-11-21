import React, { useState } from "react";
import { View, Text, Image, TouchableOpacity, ActivityIndicator, StyleSheet } from "react-native";
import * as Sharing from "expo-sharing";
import * as FileSystem from "expo-file-system/legacy";
import { COLORS, SPACING, RADIUS } from "../styles/theme";

export default function ImagePreview({ originalUri, annotatedUri, loading, onClear }) {
  const [activeTab, setActiveTab] = useState("annotated"); // 'annotated' or 'original'

  if (!originalUri && !annotatedUri && !loading) {
    return null;
  }

  const displayedUri = activeTab === "annotated" && annotatedUri ? annotatedUri : originalUri;

  const handleShare = async () => {
    if (!annotatedUri) return;

    try {
      if (annotatedUri.startsWith("data:")) {
        // Convert base64 data URI to temporary local file for sharing
        const base64Data = annotatedUri.split(",")[1];
        const tempUri = `${FileSystem.cacheDirectory}yolo_detection_${Date.now()}.jpg`;
        await FileSystem.writeAsStringAsync(tempUri, base64Data, {
          encoding: FileSystem.EncodingType.Base64,
        });
        await Sharing.shareAsync(tempUri);
      } else {
        await Sharing.shareAsync(annotatedUri);
      }
    } catch (err) {
      console.warn("Share error:", err);
    }
  };

  return (
    <View style={styles.card}>
      {/* Tab Switcher if annotated result exists */}
      {annotatedUri && (
        <View style={styles.tabsRow}>
          <TouchableOpacity
            style={[styles.tab, activeTab === "annotated" && styles.tabActive]}
            onPress={() => setActiveTab("annotated")}
          >
            <Text style={[styles.tabText, activeTab === "annotated" && styles.tabTextActive]}>
              🎯 YOLO Detection
            </Text>
          </TouchableOpacity>

          <TouchableOpacity
            style={[styles.tab, activeTab === "original" && styles.tabActive]}
            onPress={() => setActiveTab("original")}
          >
            <Text style={[styles.tabText, activeTab === "original" && styles.tabTextActive]}>
              📷 Original Photo
            </Text>
          </TouchableOpacity>
        </View>
      )}

      {/* Image Container */}
      <View style={styles.imageWrapper}>
        {displayedUri ? (
          <Image
            source={{ uri: displayedUri }}
            style={styles.image}
            resizeMode="contain"
          />
        ) : (
          <View style={styles.placeholder}>
            <Text style={styles.placeholderText}>No image selected</Text>
          </View>
        )}

        {/* Loading Overlay */}
        {loading && (
          <View style={styles.loadingOverlay}>
            <ActivityIndicator size="large" color={COLORS.primaryLight} />
            <Text style={styles.loadingText}>Running YOLO Inference...</Text>
            <Text style={styles.loadingSubtext}>Recognizing Isaac in photo</Text>
          </View>
        )}
      </View>

      {/* Action Footer */}
      <View style={styles.actionRow}>
        {annotatedUri && (
          <TouchableOpacity style={styles.btnShare} onPress={handleShare}>
            <Text style={styles.btnShareText}>💾 Save / Share Result</Text>
          </TouchableOpacity>
        )}

        <TouchableOpacity style={styles.btnClear} onPress={onClear} disabled={loading}>
          <Text style={styles.btnClearText}>✕ Clear</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  card: {
    backgroundColor: COLORS.surface,
    borderRadius: RADIUS.md,
    borderWidth: 1,
    borderColor: COLORS.border,
    marginHorizontal: SPACING.md,
    marginVertical: SPACING.sm,
    overflow: "hidden",
  },
  tabsRow: {
    flexDirection: "row",
    backgroundColor: COLORS.surfaceLight,
    borderBottomWidth: 1,
    borderBottomColor: COLORS.border,
  },
  tab: {
    flex: 1,
    paddingVertical: SPACING.sm + 2,
    alignItems: "center",
  },
  tabActive: {
    backgroundColor: COLORS.surface,
    borderBottomWidth: 2,
    borderBottomColor: COLORS.primary,
  },
  tabText: {
    fontSize: 12,
    fontWeight: "600",
    color: COLORS.textMuted,
  },
  tabTextActive: {
    color: COLORS.text,
  },
  imageWrapper: {
    width: "100%",
    height: 320,
    backgroundColor: "#0B0F19",
    position: "relative",
    justifyContent: "center",
    alignItems: "center",
  },
  image: {
    width: "100%",
    height: "100%",
  },
  placeholder: {
    alignItems: "center",
    justifyContent: "center",
  },
  placeholderText: {
    color: COLORS.textMuted,
    fontSize: 13,
  },
  loadingOverlay: {
    ...StyleSheet.absoluteFillObject,
    backgroundColor: "rgba(15, 23, 42, 0.85)",
    alignItems: "center",
    justifyContent: "center",
  },
  loadingText: {
    fontSize: 14,
    fontWeight: "700",
    color: COLORS.text,
    marginTop: SPACING.sm,
  },
  loadingSubtext: {
    fontSize: 12,
    color: COLORS.textSecondary,
    marginTop: 2,
  },
  actionRow: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    padding: SPACING.sm,
    borderTopWidth: 1,
    borderTopColor: COLORS.border,
  },
  btnShare: {
    backgroundColor: COLORS.surfaceLight,
    paddingHorizontal: SPACING.md,
    paddingVertical: SPACING.xs + 2,
    borderRadius: RADIUS.sm,
  },
  btnShareText: {
    fontSize: 12,
    fontWeight: "600",
    color: COLORS.text,
  },
  btnClear: {
    paddingHorizontal: SPACING.md,
    paddingVertical: SPACING.xs + 2,
  },
  btnClearText: {
    fontSize: 12,
    color: COLORS.textMuted,
  },
});
