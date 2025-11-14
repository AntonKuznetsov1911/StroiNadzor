/**
 * Карточка проверки/осмотра
 */
import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';
import { colors } from '../../theme/colors';
import { spacing } from '../../theme/spacing';
import { typography } from '../../theme/typography';
import { formatDate, formatTime } from '../../utils/date';

interface InspectionCardProps {
  inspection: {
    id: number;
    inspection_date: string;
    location: string;
    result: string;
    defects_count?: number;
    photos_count?: number;
    inspector_name?: string;
  };
  onPress?: () => void;
}

const RESULT_CONFIG: Record<string, { label: string; color: string }> = {
  passed: { label: 'Соответствует', color: colors.success.main },
  failed: { label: 'Не соответствует', color: colors.error.main },
  with_remarks: { label: 'С замечаниями', color: colors.warning.main },
  pending: { label: 'Ожидает проверки', color: colors.info.main },
};

export const InspectionCard: React.FC<InspectionCardProps> = ({
  inspection,
  onPress,
}) => {
  const resultConfig = RESULT_CONFIG[inspection.result] || RESULT_CONFIG.pending;
  const inspectionDate = new Date(inspection.inspection_date);

  return (
    <TouchableOpacity
      style={styles.card}
      onPress={onPress}
      disabled={!onPress}
      activeOpacity={0.7}
    >
      <View style={styles.header}>
        <View style={styles.dateContainer}>
          <Text style={styles.day}>{inspectionDate.getDate()}</Text>
          <Text style={styles.monthYear}>
            {inspectionDate.toLocaleDateString('ru-RU', {
              month: 'short',
              year: 'numeric',
            })}
          </Text>
        </View>

        <View style={styles.mainInfo}>
          <Text style={styles.location} numberOfLines={1}>
            {inspection.location}
          </Text>
          <Text style={styles.time}>{formatTime(inspectionDate)}</Text>
        </View>

        <View
          style={[styles.resultBadge, { backgroundColor: resultConfig.color }]}
        >
          <Text style={styles.resultText}>{resultConfig.label}</Text>
        </View>
      </View>

      <View style={styles.footer}>
        <View style={styles.stats}>
          {inspection.defects_count !== undefined && (
            <View style={styles.stat}>
              <Text style={styles.statValue}>{inspection.defects_count}</Text>
              <Text style={styles.statLabel}>дефектов</Text>
            </View>
          )}

          {inspection.photos_count !== undefined && (
            <View style={styles.stat}>
              <Text style={styles.statValue}>{inspection.photos_count}</Text>
              <Text style={styles.statLabel}>фото</Text>
            </View>
          )}
        </View>

        {inspection.inspector_name && (
          <Text style={styles.inspector} numberOfLines={1}>
            Инспектор: {inspection.inspector_name}
          </Text>
        )}
      </View>
    </TouchableOpacity>
  );
};

const styles = StyleSheet.create({
  card: {
    backgroundColor: colors.neutral.white,
    borderRadius: spacing.borderRadius.md,
    padding: spacing.md,
    marginBottom: spacing.md,
    elevation: 2,
    shadowColor: colors.neutral.black,
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: spacing.md,
  },
  dateContainer: {
    width: 60,
    alignItems: 'center',
    marginRight: spacing.md,
  },
  day: {
    fontSize: typography.fontSize.xxl,
    fontWeight: typography.fontWeight.bold,
    color: colors.primary.main,
  },
  monthYear: {
    fontSize: typography.fontSize.xs,
    color: colors.neutral[500],
    textTransform: 'uppercase',
  },
  mainInfo: {
    flex: 1,
    marginRight: spacing.sm,
  },
  location: {
    fontSize: typography.fontSize.md,
    fontWeight: typography.fontWeight.semibold,
    color: colors.neutral[900],
    marginBottom: spacing.xs,
  },
  time: {
    fontSize: typography.fontSize.sm,
    color: colors.neutral[600],
  },
  resultBadge: {
    paddingHorizontal: spacing.sm,
    paddingVertical: spacing.xs,
    borderRadius: spacing.borderRadius.sm,
  },
  resultText: {
    fontSize: typography.fontSize.xs,
    fontWeight: typography.fontWeight.medium,
    color: colors.neutral.white,
  },
  footer: {
    borderTopWidth: 1,
    borderTopColor: colors.neutral[200],
    paddingTop: spacing.sm,
  },
  stats: {
    flexDirection: 'row',
    marginBottom: spacing.sm,
  },
  stat: {
    flexDirection: 'row',
    alignItems: 'baseline',
    marginRight: spacing.lg,
  },
  statValue: {
    fontSize: typography.fontSize.lg,
    fontWeight: typography.fontWeight.bold,
    color: colors.primary.main,
    marginRight: spacing.xs,
  },
  statLabel: {
    fontSize: typography.fontSize.sm,
    color: colors.neutral[600],
  },
  inspector: {
    fontSize: typography.fontSize.sm,
    color: colors.neutral[500],
  },
});
