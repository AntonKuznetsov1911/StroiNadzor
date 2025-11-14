/**
 * Чекбокс
 */
import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';
import { colors } from '../../theme/colors';
import { spacing } from '../../theme/spacing';
import { typography } from '../../theme/typography';

interface CheckboxProps {
  checked: boolean;
  onChange: (checked: boolean) => void;
  label?: string;
  disabled?: boolean;
  error?: string;
}

export const Checkbox: React.FC<CheckboxProps> = ({
  checked,
  onChange,
  label,
  disabled = false,
  error,
}) => {
  const handlePress = () => {
    if (!disabled) {
      onChange(!checked);
    }
  };

  return (
    <View style={styles.container}>
      <TouchableOpacity
        style={styles.checkboxContainer}
        onPress={handlePress}
        disabled={disabled}
        activeOpacity={0.7}
      >
        <View
          style={[
            styles.checkbox,
            checked && styles.checkboxChecked,
            disabled && styles.checkboxDisabled,
            error && styles.checkboxError,
          ]}
        >
          {checked && <Text style={styles.checkmark}>✓</Text>}
        </View>

        {label && (
          <Text
            style={[
              styles.label,
              disabled && styles.labelDisabled,
              error && styles.labelError,
            ]}
          >
            {label}
          </Text>
        )}
      </TouchableOpacity>

      {error && <Text style={styles.error}>{error}</Text>}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    marginBottom: spacing.md,
  },
  checkboxContainer: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  checkbox: {
    width: 24,
    height: 24,
    borderWidth: 2,
    borderColor: colors.neutral[400],
    borderRadius: spacing.borderRadius.sm,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: colors.neutral.white,
  },
  checkboxChecked: {
    backgroundColor: colors.primary.main,
    borderColor: colors.primary.main,
  },
  checkboxDisabled: {
    backgroundColor: colors.neutral[100],
    borderColor: colors.neutral[300],
  },
  checkboxError: {
    borderColor: colors.error.main,
  },
  checkmark: {
    color: colors.neutral.white,
    fontSize: typography.fontSize.md,
    fontWeight: typography.fontWeight.bold,
  },
  label: {
    marginLeft: spacing.sm,
    fontSize: typography.fontSize.md,
    color: colors.neutral[900],
  },
  labelDisabled: {
    color: colors.neutral[500],
  },
  labelError: {
    color: colors.error.main,
  },
  error: {
    fontSize: typography.fontSize.sm,
    color: colors.error.main,
    marginTop: spacing.xs,
    marginLeft: 32,
  },
});
