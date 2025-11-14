/**
 * Карточка дефекта
 */
import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity, Image } from 'react-native';
import { colors } from '../../theme/colors';
import { spacing } from '../../theme/spacing';
import { typography } from '../../theme/typography';

interface DefectCardProps {
  defect: {
    id: number;
    defect_type: string;
    severity: string;
    description: string;
    confidence_score?: number;
    photo_url?: string;
  };
  onPress?: () => void;
}

const DEFECT_TYPES_RU: Record<string, string> = {
  crack: 'Трещина',
  deviation: 'Отклонение',
  reinforcement: 'Армирование',
  welding: 'Сварка',
  waterproofing: 'Гидроизоляция',
  concrete_quality: 'Качество бетона',
  other: 'Другое',
};

const SEVERITY_CONFIG: Record<string, { label: string; color: string }> = {
  critical: { label: 'Критический', color: colors.error.main },
  major: { label: 'Серьезный', color: colors.warning.main },
  minor: { label: 'Незначительный', color: colors.info.main },
  cosmetic: { label: 'Косметический', color: colors.neutral[400] },
};

export const DefectCard: React.FC<DefectCardProps> = ({ defect, onPress }) => {
  const severityConfig = SEVERITY_CONFIG[defect.severity] || SEVERITY_CONFIG.minor;

  return (
    <TouchableOpacity
      style={styles.card}
      onPress={onPress}
      disabled={!onPress}
      activeOpacity={0.7}
    >
      {defect.photo_url && (
        <Image source={{ uri: defect.photo_url }} style={styles.image} />
      )}

      <View style={styles.content}>
        <View style={styles.header}>
          <Text style={styles.type}>
            {DEFECT_TYPES_RU[defect.defect_type] || defect.defect_type}
          </Text>
          <View
            style={[
              styles.severityBadge,
              { backgroundColor: severityConfig.color },
            ]}
          >
            <Text style={styles.severityText}>{severityConfig.label}</Text>
          </View>
        </View>

        <Text style={styles.description} numberOfLines={2}>
          {defect.description}
        </Text>

        {defect.confidence_score && (
          <View style={styles.footer}>
            <Text style={styles.confidence}>
              Уверенность: {Math.round(defect.confidence_score * 100)}%
            </Text>
          </View>
        )}
      </View>
    </TouchableOpacity>
  );
};

const styles = StyleSheet.create({
  card: {
    backgroundColor: colors.neutral.white,
    borderRadius: spacing.borderRadius.md,
    marginBottom: spacing.md,
    overflow: 'hidden',
    elevation: 2,
    shadowColor: colors.neutral.black,
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
  },
  image: {
    width: '100%',
    height: 200,
    resizeMode: 'cover',
  },
  content: {
    padding: spacing.md,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: spacing.sm,
  },
  type: {
    fontSize: typography.fontSize.lg,
    fontWeight: typography.fontWeight.semibold,
    color: colors.neutral[900],
  },
  severityBadge: {
    paddingHorizontal: spacing.sm,
    paddingVertical: spacing.xs,
    borderRadius: spacing.borderRadius.sm,
  },
  severityText: {
    fontSize: typography.fontSize.xs,
    fontWeight: typography.fontWeight.medium,
    color: colors.neutral.white,
  },
  description: {
    fontSize: typography.fontSize.md,
    color: colors.neutral[600],
    lineHeight: typography.fontSize.md * typography.lineHeight.normal,
  },
  footer: {
    marginTop: spacing.sm,
    paddingTop: spacing.sm,
    borderTopWidth: 1,
    borderTopColor: colors.neutral[200],
  },
  confidence: {
    fontSize: typography.fontSize.sm,
    color: colors.neutral[500],
  },
});
