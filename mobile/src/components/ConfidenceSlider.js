import React from "react";
import { View, Text, TouchableOpacity, StyleSheet } from "react-native";
import Slider from "@react-native-community/slider";
import { COLORS, SPACING, RADIUS } from "../styles/theme";

export default function ConfidenceSlider({ confidence, onConfidenceChange }) {
  const percentage = Math.round(confidence * 100);

  const adjustConfidence = (delta) => {
    const nextVal = Math.min(0.95, Math.max(0.05, Math.round((confidence + delta) * 100) / 100));
    onConfidenceChange(nextVal);
  };

  return (
    <View style={styles.card}>
      <View style={styles.headerRow}>
        <Text style={styles.label}>Confidence Threshold</Text>
        <View style={styles.badge}>
          <Text style={styles.badgeText}>{percentage}% ({confidence.toFixed(2)})</Text>
        </View>
      </View>

      <Slider
        style={styles.slider}
        minimumValue={0.05}
        maximumValue={0.95}
        step={0.05}
        value={confidence}
        onValueChange={onConfidenceChange}
        minimumTrackTintColor={COLORS.primary}
        maximumTrackTintColor={COLORS.surfaceLight}
        thumbTintColor={COLORS.primaryLight}
      />

      <View style={styles.labelsRow}>
        <Text style={styles.subtext}>5% (Permissive)</Text>
        <View style={styles.quickButtons}>
          <TouchableOpacity
            style={styles.btnStep}
            onPress={() => adjustConfidence(-0.05)}
          >
            <Text style={styles.btnStepText}>-5%</Text>
          </TouchableOpacity>
          <TouchableOpacity
            style={styles.btnStep}
            onPress={() => adjustConfidence(0.05)}
          >
            <Text style={styles.btnStepText}>+5%</Text>
          </TouchableOpacity>
        </View>
        <Text style={styles.subtext}>95% (Strict)</Text>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  card: {
    backgroundColor: COLORS.surface,
    padding: SPACING.md,
    borderRadius: RADIUS.md,
    borderWidth: 1,
    borderColor: COLORS.border,
    marginHorizontal: SPACING.md,
    marginVertical: SPACING.sm,
  },
  headerRow: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: SPACING.sm,
  },
  label: {
    fontSize: 14,
    fontWeight: "600",
    color: COLORS.text,
  },
  badge: {
    backgroundColor: "rgba(79, 70, 229, 0.2)",
    borderWidth: 1,
    borderColor: COLORS.primary,
    paddingHorizontal: SPACING.sm,
    paddingVertical: 3,
    borderRadius: RADIUS.full,
  },
  badgeText: {
    fontSize: 12,
    fontWeight: "700",
    color: COLORS.primaryLight,
  },
  slider: {
    width: "100%",
    height: 36,
  },
  labelsRow: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    marginTop: 2,
  },
  subtext: {
    fontSize: 11,
    color: COLORS.textMuted,
  },
  quickButtons: {
    flexDirection: "row",
    gap: 6,
  },
  btnStep: {
    backgroundColor: COLORS.surfaceLight,
    paddingHorizontal: 8,
    paddingVertical: 3,
    borderRadius: RADIUS.sm,
  },
  btnStepText: {
    fontSize: 11,
    fontWeight: "600",
    color: COLORS.textSecondary,
  },
});
