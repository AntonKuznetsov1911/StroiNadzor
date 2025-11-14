/**
 * Прогресс-бар
 */
import React from 'react';
import { View, Text, StyleSheet, ViewStyle } from 'react-native';
import { colors } from '../../theme/colors';
import { spacing } from '../../theme/spacing';
import { typography } from '../../theme/typography';

interface ProgressBarProps {
  progress: number; // 0-100
  height?: number;
  color?: string;
  showLabel?: boolean;
  label?: string;
  style?: ViewStyle;
}

export const ProgressBar: React.FC<ProgressBarProps> = ({
  progress,
  height = 8,
  color = colors.primary.main,
  showLabel = false,
  label,
  style,
}) => {
  // Ограничиваем прогресс между 0 и 100
  const clampedProgress = Math.max(0, Math.min(100, progress));

  return (
    <View style={[styles.container, style]}>
      {showLabel && (
        <View style={styles.labelContainer}>
          {label && <Text style={styles.label}>{label}</Text>}
          <Text style={styles.percentage}>{Math.round(clampedProgress)}%</Text>
        </View>
      )}

      <View style={[styles.track, { height }]}>
        <View
          style={[
            styles.fill,
            {
              width: `${clampedProgress}%`,
              backgroundColor: color,
              height,
            },
          ]}
        />
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    width: '100%',
  },
  labelContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: spacing.xs,
  },
  label: {
    fontSize: typography.fontSize.sm,
    color: colors.neutral[700],
    fontWeight: typography.fontWeight.medium,
  },
  percentage: {
    fontSize: typography.fontSize.sm,
    color: colors.neutral[600],
    fontWeight: typography.fontWeight.semibold,
  },
  track: {
    width: '100%',
    backgroundColor: colors.neutral[200],
    borderRadius: spacing.borderRadius.full,
    overflow: 'hidden',
  },
  fill: {
    borderRadius: spacing.borderRadius.full,
  },
});
