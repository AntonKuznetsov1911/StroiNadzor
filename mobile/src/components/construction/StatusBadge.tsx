/**
 * Бейдж статуса
 */
import React from 'react';
import { View, Text, StyleSheet, ViewStyle } from 'react-native';
import { colors } from '../../theme/colors';
import { spacing } from '../../theme/spacing';
import { typography } from '../../theme/typography';

type StatusType = 'success' | 'error' | 'warning' | 'info' | 'default';

interface StatusBadgeProps {
  status: StatusType;
  label: string;
  size?: 'small' | 'medium' | 'large';
  style?: ViewStyle;
}

const STATUS_COLORS: Record<StatusType, { bg: string; text: string }> = {
  success: { bg: colors.success.light, text: colors.success.dark },
  error: { bg: colors.error.light, text: colors.error.dark },
  warning: { bg: colors.warning.light, text: colors.warning.dark },
  info: { bg: colors.info.light, text: colors.info.dark },
  default: { bg: colors.neutral[100], text: colors.neutral[700] },
};

const SIZE_CONFIG = {
  small: {
    paddingHorizontal: spacing.xs,
    paddingVertical: spacing.xs / 2,
    fontSize: typography.fontSize.xs,
  },
  medium: {
    paddingHorizontal: spacing.sm,
    paddingVertical: spacing.xs,
    fontSize: typography.fontSize.sm,
  },
  large: {
    paddingHorizontal: spacing.md,
    paddingVertical: spacing.sm,
    fontSize: typography.fontSize.md,
  },
};

export const StatusBadge: React.FC<StatusBadgeProps> = ({
  status,
  label,
  size = 'medium',
  style,
}) => {
  const colorConfig = STATUS_COLORS[status];
  const sizeConfig = SIZE_CONFIG[size];

  return (
    <View
      style={[
        styles.badge,
        {
          backgroundColor: colorConfig.bg,
          paddingHorizontal: sizeConfig.paddingHorizontal,
          paddingVertical: sizeConfig.paddingVertical,
        },
        style,
      ]}
    >
      <Text
        style={[
          styles.text,
          {
            color: colorConfig.text,
            fontSize: sizeConfig.fontSize,
          },
        ]}
      >
        {label}
      </Text>
    </View>
  );
};

const styles = StyleSheet.create({
  badge: {
    borderRadius: spacing.borderRadius.sm,
    alignSelf: 'flex-start',
  },
  text: {
    fontWeight: typography.fontWeight.semibold,
  },
});
