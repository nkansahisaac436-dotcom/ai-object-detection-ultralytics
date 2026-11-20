import React from "react";
import { View, Text, StyleSheet } from "react-native";
import { COLORS, SPACING, RADIUS } from "../styles/theme";

export default function DetectionsList({ results }) {
  if (!results) return null;

  const { detections = [], count = 0, inferenceMs = 0, imageWidth = 0, imageHeight = 0 } = results;

  return (
    <View style={styles.container}>
      {/* Metrics Row */}
      <View style={styles.metricsGrid}>
        <View style={styles.metricCard}>
          <Text style={styles.metricVal}>{count}</Text>
          <Text style={styles.metricLabel}>Detections</Text>
        </View>

        <View style={styles.metricCard}>
          <Text style={styles.metricVal}>{inferenceMs} ms</Text>
          <Text style={styles.metricLabel}>Speed</Text>
        </View>

        <View style={styles.metricCard}>
          <Text style={styles.metricVal}>
            {imageWidth > 0 ? `${imageWidth}x${imageHeight}` : "--"}
          </Text>
          <Text style={styles.metricLabel}>Dimensions</Text>
        </View>
      </View>

      {/* Detections Breakdown */}
      <View style={styles.breakdownCard}>
        <Text style={styles.sectionTitle}>Detected Classes</Text>

        {detections.length === 0 ? (
          <View style={styles.emptyState}>
            <Text style={styles.emptyIcon}>🔍</Text>
            <Text style={styles.emptyText}>No objects found matching this confidence threshold.</Text>
            <Text style={styles.emptySubtext}>Try lowering the confidence slider.</Text>
          </View>
        ) : (
          detections.map((det, index) => {
            const pct = Math.round(det.confidence * 100);
            const bboxStr = det.bbox ? det.bbox.map((v) => Math.round(v)).join(", ") : "N/A";

            return (
              <View key={index} style={styles.detRow}>
                <View style={styles.detLeft}>
                  <View style={styles.classBadge}>
                    <Text style={styles.className}>{det.class_name || "Isaac"}</Text>
                  </View>
                  <Text style={styles.bboxText}>Box: [{bboxStr}]</Text>
                </View>

                <View style={styles.detRight}>
                  <Text style={styles.scoreText}>{pct}%</Text>
                  <View style={styles.scoreBarTrack}>
                    <View style={[styles.scoreBarFill, { width: `${pct}%` }]} />
                  </View>
                </View>
              </View>
            );
          })
        )}
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    marginHorizontal: SPACING.md,
    marginVertical: SPACING.sm,
  },
  metricsGrid: {
    flexDirection: "row",
    gap: SPACING.sm,
    marginBottom: SPACING.sm,
  },
  metricCard: {
    flex: 1,
    backgroundColor: COLORS.surface,
    padding: SPACING.sm + 2,
    borderRadius: RADIUS.md,
    borderWidth: 1,
    borderColor: COLORS.border,
    alignItems: "center",
  },
  metricVal: {
    fontSize: 16,
    fontWeight: "700",
    color: COLORS.accentLight,
  },
  metricLabel: {
    fontSize: 11,
    color: COLORS.textMuted,
    marginTop: 2,
  },
  breakdownCard: {
    backgroundColor: COLORS.surface,
    padding: SPACING.md,
    borderRadius: RADIUS.md,
    borderWidth: 1,
    borderColor: COLORS.border,
  },
  sectionTitle: {
    fontSize: 14,
    fontWeight: "700",
    color: COLORS.text,
    marginBottom: SPACING.sm,
  },
  emptyState: {
    alignItems: "center",
    paddingVertical: SPACING.md,
  },
  emptyIcon: {
    fontSize: 28,
    marginBottom: 6,
  },
  emptyText: {
    fontSize: 13,
    color: COLORS.textSecondary,
    textAlign: "center",
  },
  emptySubtext: {
    fontSize: 11,
    color: COLORS.textMuted,
    marginTop: 2,
  },
  detRow: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    paddingVertical: SPACING.sm,
    borderBottomWidth: 1,
    borderBottomColor: "rgba(255, 255, 255, 0.05)",
  },
  detLeft: {
    flex: 1,
  },
  classBadge: {
    alignSelf: "flex-start",
    backgroundColor: "rgba(16, 185, 129, 0.15)",
    borderWidth: 1,
    borderColor: COLORS.accent,
    paddingHorizontal: 8,
    paddingVertical: 2,
    borderRadius: RADIUS.sm,
    marginBottom: 4,
  },
  className: {
    fontSize: 13,
    fontWeight: "700",
    color: COLORS.accentLight,
  },
  bboxText: {
    fontSize: 11,
    color: COLORS.textMuted,
    fontFamily: "monospace",
  },
  detRight: {
    alignItems: "flex-end",
    width: 80,
  },
  scoreText: {
    fontSize: 14,
    fontWeight: "700",
    color: COLORS.text,
    marginBottom: 4,
  },
  scoreBarTrack: {
    width: "100%",
    height: 4,
    backgroundColor: COLORS.surfaceLight,
    borderRadius: 2,
    overflow: "hidden",
  },
  scoreBarFill: {
    height: "100%",
    backgroundColor: COLORS.accent,
  },
});
