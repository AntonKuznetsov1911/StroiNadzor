/**
 * Радио-кнопки
 */
import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';
import { colors } from '../../theme/colors';
import { spacing } from '../../theme/spacing';
import { typography } from '../../theme/typography';

export interface RadioOption {
  label: string;
  value: string | number;
}

interface RadioButtonProps {
  options: RadioOption[];
  value?: string | number;
  onChange: (value: string | number) => void;
  label?: string;
  disabled?: boolean;
  error?: string;
  direction?: 'vertical' | 'horizontal';
}

export const RadioButton: React.FC<RadioButtonProps> = ({
  options,
  value,
  onChange,
  label,
  disabled = false,
  error,
  direction = 'vertical',
}) => {
  const handlePress = (optionValue: string | number) => {
    if (!disabled) {
      onChange(optionValue);
    }
  };

  return (
    <View style={styles.container}>
      {label && <Text style={styles.groupLabel}>{label}</Text>}

      <View
        style={[
          styles.optionsContainer,
          direction === 'horizontal' && styles.optionsContainerHorizontal,
        ]}
      >
        {options.map((option) => {
          const isSelected = option.value === value;

          return (
            <TouchableOpacity
              key={option.value}
              style={[
                styles.option,
                direction === 'horizontal' && styles.optionHorizontal,
              ]}
              onPress={() => handlePress(option.value)}
              disabled={disabled}
              activeOpacity={0.7}
            >
              <View
                style={[
                  styles.radio,
                  isSelected && styles.radioSelected,
                  disabled && styles.radioDisabled,
                  error && styles.radioError,
                ]}
              >
                {isSelected && <View style={styles.radioInner} />}
              </View>

              <Text
                style={[
                  styles.label,
                  disabled && styles.labelDisabled,
                  error && styles.labelError,
                ]}
              >
                {option.label}
              </Text>
            </TouchableOpacity>
          );
        })}
      </View>

      {error && <Text style={styles.error}>{error}</Text>}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    marginBottom: spacing.md,
  },
  groupLabel: {
    fontSize: typography.fontSize.md,
    fontWeight: typography.fontWeight.medium,
    color: colors.neutral[700],
    marginBottom: spacing.sm,
  },
  optionsContainer: {
    gap: spacing.sm,
  },
  optionsContainerHorizontal: {
    flexDirection: 'row',
    flexWrap: 'wrap',
  },
  option: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: spacing.xs,
  },
  optionHorizontal: {
    marginRight: spacing.lg,
  },
  radio: {
    width: 24,
    height: 24,
    borderWidth: 2,
    borderColor: colors.neutral[400],
    borderRadius: spacing.borderRadius.full,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: colors.neutral.white,
  },
  radioSelected: {
    borderColor: colors.primary.main,
  },
  radioDisabled: {
    backgroundColor: colors.neutral[100],
    borderColor: colors.neutral[300],
  },
  radioError: {
    borderColor: colors.error.main,
  },
  radioInner: {
    width: 12,
    height: 12,
    borderRadius: spacing.borderRadius.full,
    backgroundColor: colors.primary.main,
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
  },
});
