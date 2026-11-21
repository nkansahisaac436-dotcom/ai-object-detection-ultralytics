import React from "react";
import {
  Modal,
  View,
  Text,
  Image,
  TouchableOpacity,
  ScrollView,
  StyleSheet,
  SafeAreaView
} from "react-native";
import * as Sharing from "expo-sharing";
import * as FileSystem from "expo-file-system/legacy";
import { COLORS, SPACING, RADIUS } from "../styles/theme";

export default function HistoryModal({
  visible,
  onClose,
  history = [],
  onSelectHistoryItem,
  onClearHistory
}) {
  const handleShareItem = async (annotatedUri) => {
    if (!annotatedUri) return;
    try {
      if (annotatedUri.startsWith("data:")) {
        const base64Data = annotatedUri.split(",")[1];
        const tempUri = `${FileSystem.cacheDirectory}isaac_history_${Date.now()}.jpg`;
        await FileSystem.writeAsStringAsync(tempUri, base64Data, {
          encoding: FileSystem.EncodingType.Base64
        });
        await Sharing.shareAsync(tempUri);
      } else {
        await Sharing.shareAsync(annotatedUri);
      }
    } catch (err) {
      console.warn("Share history item error:", err);
    }
  };

  return (
    <Modal visible={visible} animationType="slide" transparent={false} onRequestClose={onClose}>
      <SafeAreaView style={styles.safeArea}>
        {/* Header */}
        <View style={styles.header}>
          <View>
            <Text style={styles.headerTitle}>Tested Images History</Text>
            <Text style={styles.headerSubtitle}>
              {history.length} {history.length === 1 ? "test" : "tests"} recorded this session
            </Text>
          </View>
          <TouchableOpacity style={styles.btnClose} onPress={onClose}>
            <Text style={styles.btnCloseText}>✕ Close</Text>
          </TouchableOpacity>
        </View>

        {/* Content */}
        {history.length === 0 ? (
          <View style={styles.emptyContainer}>
            <Text style={styles.emptyIcon}>📷</Text>
            <Text style={styles.emptyTitle}>No Tested Images Yet</Text>
            <Text style={styles.emptyText}>
              Run YOLO detection on photos to automatically save and compare them here.
            </Text>
          </View>
        ) : (
          <ScrollView contentContainerStyle={styles.listContainer}>
            {history.map((item, index) => {
              const count = item.count || 0;
              const confPct = Math.round((item.confidence || 0.25) * 100);

              return (
                <View key={item.id || index} style={styles.card}>
                  <View style={styles.cardHeader}>
                    <View style={styles.badgeIndex}>
                      <Text style={styles.badgeIndexText}>#{history.length - index}</Text>
                    </View>
                    <Text style={styles.timestamp}>{item.timestamp}</Text>
                    <View
                      style={[
                        styles.countBadge,
                        count > 0 ? styles.countBadgeFound : styles.countBadgeZero
                      ]}
                    >
                      <Text style={styles.countBadgeText}>
                        {count > 0 ? `🎯 ${count} Isaac Detected` : "0 Detections"}
                      </Text>
                    </View>
                  </View>

                  {/* Thumbnail */}
                  <View style={styles.thumbContainer}>
                    <Image
                      source={{ uri: item.annotatedUri || item.originalUri }}
                      style={styles.thumbnail}
                      resizeMode="cover"
                    />
                  </View>

                  {/* Stats Bar */}
                  <View style={styles.statsRow}>
                    <Text style={styles.statLabel}>
                      Conf: <Text style={styles.statVal}>{confPct}%</Text>
                    </Text>
                    {item.inferenceMs ? (
                      <Text style={styles.statLabel}>
                        Speed: <Text style={styles.statVal}>{item.inferenceMs} ms</Text>
                      </Text>
                    ) : null}
                  </View>

                  {/* Card Actions */}
                  <View style={styles.cardActions}>
                    <TouchableOpacity
                      style={styles.btnView}
                      onPress={() => onSelectHistoryItem(item)}
                    >
                      <Text style={styles.btnViewText}>👁️ View in App</Text>
                    </TouchableOpacity>

                    <TouchableOpacity
                      style={styles.btnShare}
                      onPress={() => handleShareItem(item.annotatedUri)}
                    >
                      <Text style={styles.btnShareText}>💾 Save / Share</Text>
                    </TouchableOpacity>
                  </View>
                </View>
              );
            })}

            {/* Clear Button at bottom of list */}
            <TouchableOpacity style={styles.btnClearAll} onPress={onClearHistory}>
              <Text style={styles.btnClearAllText}>🗑️ Clear Detection History</Text>
            </TouchableOpacity>
          </ScrollView>
        )}
      </SafeAreaView>
    </Modal>
  );
}

const styles = StyleSheet.create({
  safeArea: {
    flex: 1,
    backgroundColor: COLORS.bg
  },
  header: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
    paddingHorizontal: SPACING.md,
    paddingVertical: SPACING.md,
    backgroundColor: COLORS.surface,
    borderBottomWidth: 1,
    borderBottomColor: COLORS.border
  },
  headerTitle: {
    fontSize: 18,
    fontWeight: "700",
    color: COLORS.text
  },
  headerSubtitle: {
    fontSize: 12,
    color: COLORS.textSecondary,
    marginTop: 2
  },
  btnClose: {
    paddingHorizontal: SPACING.sm,
    paddingVertical: 6,
    borderRadius: RADIUS.md,
    backgroundColor: COLORS.surfaceAlt
  },
  btnCloseText: {
    color: COLORS.text,
    fontWeight: "600",
    fontSize: 13
  },
  listContainer: {
    padding: SPACING.md,
    paddingBottom: 40
  },
  card: {
    backgroundColor: COLORS.surface,
    borderRadius: RADIUS.lg,
    borderWidth: 1,
    borderColor: COLORS.border,
    padding: SPACING.md,
    marginBottom: SPACING.md
  },
  cardHeader: {
    flexDirection: "row",
    alignItems: "center",
    marginBottom: SPACING.sm
  },
  badgeIndex: {
    backgroundColor: "rgba(79, 70, 229, 0.2)",
    paddingHorizontal: 8,
    paddingVertical: 2,
    borderRadius: RADIUS.sm,
    marginRight: 8
  },
  badgeIndexText: {
    color: COLORS.primaryLight,
    fontWeight: "700",
    fontSize: 12
  },
  timestamp: {
    color: COLORS.textMuted,
    fontSize: 12,
    flex: 1
  },
  countBadge: {
    paddingHorizontal: 8,
    paddingVertical: 3,
    borderRadius: RADIUS.sm
  },
  countBadgeFound: {
    backgroundColor: "rgba(16, 185, 129, 0.15)"
  },
  countBadgeZero: {
    backgroundColor: "rgba(148, 163, 184, 0.15)"
  },
  countBadgeText: {
    fontSize: 12,
    fontWeight: "600",
    color: COLORS.text
  },
  thumbContainer: {
    width: "100%",
    height: 180,
    backgroundColor: "#000",
    borderRadius: RADIUS.md,
    overflow: "hidden",
    marginVertical: SPACING.sm
  },
  thumbnail: {
    width: "100%",
    height: "100%"
  },
  statsRow: {
    flexDirection: "row",
    justifyContent: "space-between",
    paddingVertical: 4,
    marginBottom: SPACING.sm
  },
  statLabel: {
    color: COLORS.textSecondary,
    fontSize: 12
  },
  statVal: {
    color: COLORS.text,
    fontWeight: "600"
  },
  cardActions: {
    flexDirection: "row",
    gap: SPACING.sm
  },
  btnView: {
    flex: 1,
    backgroundColor: COLORS.primary,
    paddingVertical: 10,
    borderRadius: RADIUS.md,
    alignItems: "center"
  },
  btnViewText: {
    color: "#fff",
    fontWeight: "600",
    fontSize: 13
  },
  btnShare: {
    flex: 1,
    backgroundColor: COLORS.surfaceAlt,
    borderWidth: 1,
    borderColor: COLORS.border,
    paddingVertical: 10,
    borderRadius: RADIUS.md,
    alignItems: "center"
  },
  btnShareText: {
    color: COLORS.text,
    fontWeight: "600",
    fontSize: 13
  },
  btnClearAll: {
    marginTop: SPACING.sm,
    paddingVertical: 12,
    alignItems: "center",
    borderRadius: RADIUS.md,
    borderWidth: 1,
    borderColor: "rgba(239, 68, 68, 0.3)",
    backgroundColor: "rgba(239, 68, 68, 0.08)"
  },
  btnClearAllText: {
    color: COLORS.danger,
    fontWeight: "600",
    fontSize: 13
  },
  emptyContainer: {
    flex: 1,
    alignItems: "center",
    justifyContent: "center",
    padding: SPACING.xl
  },
  emptyIcon: {
    fontSize: 48,
    marginBottom: SPACING.sm
  },
  emptyTitle: {
    fontSize: 18,
    fontWeight: "700",
    color: COLORS.text,
    marginBottom: 4
  },
  emptyText: {
    fontSize: 13,
    color: COLORS.textMuted,
    textAlign: "center",
    lineHeight: 18
  }
});
