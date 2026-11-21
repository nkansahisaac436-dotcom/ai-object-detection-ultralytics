import React from "react";
import { View, Text, TouchableOpacity, StyleSheet } from "react-native";
import { COLORS, SPACING, RADIUS } from "../styles/theme";

export default function Header({
  status = "loading",
  statusMessage = "Checking server...",
  historyCount = 0,
  onOpenHistory
}) {
  const getBadgeStyle = () => {
    switch (status) {
      case "online":
        return { bg: "rgba(16, 185, 129, 0.15)", text: COLORS.accent, dot: COLORS.accent };
      case "offline":
        return { bg: "rgba(239, 68, 68, 0.15)", text: COLORS.danger, dot: COLORS.danger };
      default:
        return { bg: "rgba(245, 158, 11, 0.15)", text: COLORS.warning, dot: COLORS.warning };
    }
  };

  const badge = getBadgeStyle();

  return (
    <View style={styles.container}>
      <View style={styles.titleRow}>
        <View style={styles.iconCircle}>
          <Text style={styles.iconText}>🎯</Text>
        </View>
        <View style={styles.titleGroup}>
          <Text style={styles.title}>Isaac YOLO Detection</Text>
          <Text style={styles.subtitle}>Personal Recognition • Pentecost Univ.</Text>
        </View>
      </View>

      <View style={styles.bottomRow}>
        <View style={[styles.statusBadge, { backgroundColor: badge.bg }]}>
          <View style={[styles.statusDot, { backgroundColor: badge.dot }]} />
          <Text style={[styles.statusText, { color: badge.text }]} numberOfLines={1}>
            {statusMessage}
          </Text>
        </View>

        {onOpenHistory && (
          <TouchableOpacity style={styles.btnHistory} onPress={onOpenHistory}>
            <Text style={styles.btnHistoryText}>🕒 History ({historyCount})</Text>
          </TouchableOpacity>
        )}
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    paddingHorizontal: SPACING.md,
    paddingTop: SPACING.md,
    paddingBottom: SPACING.sm,
    backgroundColor: COLORS.surface,
    borderBottomWidth: 1,
    borderBottomColor: COLORS.border,
  },
  titleRow: {
    flexDirection: "row",
    alignItems: "center",
    marginBottom: SPACING.sm,
  },
  iconCircle: {
    width: 44,
    height: 44,
    borderRadius: RADIUS.full,
    backgroundColor: "rgba(79, 70, 229, 0.2)",
    borderWidth: 1,
    borderColor: COLORS.primary,
    alignItems: "center",
    justifyContent: "center",
    marginRight: SPACING.sm,
  },
  iconText: {
    fontSize: 22,
  },
  titleGroup: {
    flex: 1,
  },
  title: {
    fontSize: 18,
    fontWeight: "700",
    color: COLORS.text,
  },
  subtitle: {
    fontSize: 12,
    color: COLORS.textSecondary,
    marginTop: 2,
  },
  bottomRow: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
  },
  statusBadge: {
    flexDirection: "row",
    alignItems: "center",
    paddingHorizontal: SPACING.sm,
    paddingVertical: 5,
    borderRadius: RADIUS.full,
    flex: 1,
    marginRight: SPACING.sm,
  },
  statusDot: {
    width: 7,
    height: 7,
    borderRadius: RADIUS.full,
    marginRight: 6,
  },
  statusText: {
    fontSize: 12,
    fontWeight: "600",
  },
  btnHistory: {
    paddingHorizontal: 12,
    paddingVertical: 5,
    borderRadius: RADIUS.full,
    backgroundColor: "rgba(79, 70, 229, 0.15)",
    borderWidth: 1,
    borderColor: COLORS.primary,
  },
  btnHistoryText: {
    color: COLORS.primaryLight,
    fontSize: 12,
    fontWeight: "600",
  },
});
