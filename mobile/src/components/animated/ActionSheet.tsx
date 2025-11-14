/**
 * Action Sheet - меню действий снизу
 */
import React from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  ScrollView,
} from 'react-native';
import { BottomSheet } from './BottomSheet';
import { colors } from '../../theme/colors';
import { spacing } from '../../theme/spacing';
import { typography } from '../../theme/typography';

export interface ActionSheetOption {
  label: string;
  onPress: () => void;
  icon?: string;
  destructive?: boolean;
  disabled?: boolean;
}

interface ActionSheetProps {
  visible: boolean;
  onClose: () => void;
  title?: string;
  message?: string;
  options: ActionSheetOption[];
  cancelLabel?: string;
}

export const ActionSheet: React.FC<ActionSheetProps> = ({
  visible,
  onClose,
  title,
  message,
  options,
  cancelLabel = 'Отмена',
}) => {
  const handleOptionPress = (option: ActionSheetOption) => {
    if (!option.disabled) {
      option.onPress();
      onClose();
    }
  };

  return (
    <BottomSheet
      visible={visible}
      onClose={onClose}
      height={
        (options.length + 1) * 60 +
        (title ? 60 : 0) +
        (message ? 40 : 0) +
        spacing.xl
      }
    >
      {title && <Text style={styles.title}>{title}</Text>}
      {message && <Text style={styles.message}>{message}</Text>}

      <ScrollView style={styles.optionsContainer}>
        {options.map((option, index) => (
          <TouchableOpacity
            key={index}
            style={[
              styles.option,
              option.disabled && styles.optionDisabled,
            ]}
            onPress={() => handleOptionPress(option)}
            disabled={option.disabled}
            activeOpacity={0.7}
          >
            {option.icon && <Text style={styles.optionIcon}>{option.icon}</Text>}
            <Text
              style={[
                styles.optionLabel,
                option.destructive && styles.optionLabelDestructive,
                option.disabled && styles.optionLabelDisabled,
              ]}
            >
              {option.label}
            </Text>
          </TouchableOpacity>
        ))}
      </ScrollView>

      <TouchableOpacity style={styles.cancelButton} onPress={onClose}>
        <Text style={styles.cancelButtonText}>{cancelLabel}</Text>
      </TouchableOpacity>
    </BottomSheet>
  );
};

const styles = StyleSheet.create({
  title: {
    fontSize: typography.fontSize.xl,
    fontWeight: typography.fontWeight.bold,
    color: colors.neutral[900],
    marginBottom: spacing.sm,
    textAlign: 'center',
  },
  message: {
    fontSize: typography.fontSize.md,
    color: colors.neutral[600],
    marginBottom: spacing.md,
    textAlign: 'center',
  },
  optionsContainer: {
    maxHeight: 400,
  },
  option: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: spacing.md,
    paddingHorizontal: spacing.sm,
    borderBottomWidth: 1,
    borderBottomColor: colors.neutral[200],
  },
  optionDisabled: {
    opacity: 0.5,
  },
  optionIcon: {
    fontSize: typography.fontSize.xl,
    marginRight: spacing.md,
  },
  optionLabel: {
    fontSize: typography.fontSize.lg,
    color: colors.neutral[900],
  },
  optionLabelDestructive: {
    color: colors.error.main,
  },
  optionLabelDisabled: {
    color: colors.neutral[400],
  },
  cancelButton: {
    marginTop: spacing.md,
    paddingVertical: spacing.md,
    borderTopWidth: 1,
    borderTopColor: colors.neutral[200],
  },
  cancelButtonText: {
    fontSize: typography.fontSize.lg,
    fontWeight: typography.fontWeight.semibold,
    color: colors.neutral[700],
    textAlign: 'center',
  },
});
