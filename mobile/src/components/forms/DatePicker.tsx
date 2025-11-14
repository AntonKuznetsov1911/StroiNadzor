/**
 * Выбор даты
 */
import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  Platform,
  Modal,
} from 'react-native';
import { colors } from '../../theme/colors';
import { spacing } from '../../theme/spacing';
import { typography } from '../../theme/typography';
import { formatDate } from '../../utils/date';

interface DatePickerProps {
  label?: string;
  value?: Date;
  onChange: (date: Date) => void;
  placeholder?: string;
  required?: boolean;
  error?: string;
  minDate?: Date;
  maxDate?: Date;
  disabled?: boolean;
}

export const DatePicker: React.FC<DatePickerProps> = ({
  label,
  value,
  onChange,
  placeholder = 'Выберите дату',
  required = false,
  error,
  minDate,
  maxDate,
  disabled = false,
}) => {
  const [isVisible, setIsVisible] = useState(false);

  const handlePress = () => {
    if (!disabled) {
      setIsVisible(true);
    }
  };

  const handleConfirm = (date: Date) => {
    onChange(date);
    setIsVisible(false);
  };

  return (
    <View style={styles.container}>
      {label && (
        <Text style={styles.label}>
          {label}
          {required && <Text style={styles.required}> *</Text>}
        </Text>
      )}

      <TouchableOpacity
        style={[
          styles.input,
          error && styles.inputError,
          disabled && styles.inputDisabled,
        ]}
        onPress={handlePress}
        disabled={disabled}
      >
        <Text
          style={[
            styles.inputText,
            !value && styles.placeholder,
            disabled && styles.textDisabled,
          ]}
        >
          {value ? formatDate(value) : placeholder}
        </Text>
        <Text style={styles.icon}>📅</Text>
      </TouchableOpacity>

      {error && <Text style={styles.error}>{error}</Text>}

      {/* Простой Modal для выбора даты */}
      {/* В реальном приложении используйте @react-native-community/datetimepicker */}
      <Modal visible={isVisible} transparent animationType="fade">
        <TouchableOpacity
          style={styles.modalOverlay}
          activeOpacity={1}
          onPress={() => setIsVisible(false)}
        >
          <View style={styles.modalContent}>
            <Text style={styles.modalTitle}>Выбор даты</Text>
            <Text style={styles.modalSubtitle}>
              В реальном приложении здесь будет @react-native-community/datetimepicker
            </Text>
            <TouchableOpacity
              style={styles.modalButton}
              onPress={() => handleConfirm(new Date())}
            >
              <Text style={styles.modalButtonText}>Выбрать сегодня</Text>
            </TouchableOpacity>
            <TouchableOpacity
              style={[styles.modalButton, styles.modalButtonSecondary]}
              onPress={() => setIsVisible(false)}
            >
              <Text style={styles.modalButtonTextSecondary}>Отмена</Text>
            </TouchableOpacity>
          </View>
        </TouchableOpacity>
      </Modal>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    marginBottom: spacing.md,
  },
  label: {
    fontSize: typography.fontSize.md,
    fontWeight: typography.fontWeight.medium,
    color: colors.neutral[700],
    marginBottom: spacing.xs,
  },
  required: {
    color: colors.error.main,
  },
  input: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    height: 48,
    borderWidth: 1,
    borderColor: colors.neutral[300],
    borderRadius: spacing.borderRadius.md,
    paddingHorizontal: spacing.md,
    backgroundColor: colors.neutral.white,
  },
  inputError: {
    borderColor: colors.error.main,
  },
  inputDisabled: {
    backgroundColor: colors.neutral[100],
    borderColor: colors.neutral[200],
  },
  inputText: {
    flex: 1,
    fontSize: typography.fontSize.md,
    color: colors.neutral[900],
  },
  placeholder: {
    color: colors.neutral[400],
  },
  textDisabled: {
    color: colors.neutral[500],
  },
  icon: {
    fontSize: typography.fontSize.lg,
  },
  error: {
    fontSize: typography.fontSize.sm,
    color: colors.error.main,
    marginTop: spacing.xs,
  },
  modalOverlay: {
    flex: 1,
    backgroundColor: 'rgba(0, 0, 0, 0.5)',
    justifyContent: 'center',
    alignItems: 'center',
  },
  modalContent: {
    backgroundColor: colors.neutral.white,
    borderRadius: spacing.borderRadius.lg,
    padding: spacing.xl,
    width: '80%',
    maxWidth: 400,
  },
  modalTitle: {
    fontSize: typography.fontSize.xl,
    fontWeight: typography.fontWeight.bold,
    color: colors.neutral[900],
    marginBottom: spacing.sm,
    textAlign: 'center',
  },
  modalSubtitle: {
    fontSize: typography.fontSize.sm,
    color: colors.neutral[600],
    textAlign: 'center',
    marginBottom: spacing.lg,
  },
  modalButton: {
    backgroundColor: colors.primary.main,
    paddingVertical: spacing.md,
    borderRadius: spacing.borderRadius.md,
    marginBottom: spacing.sm,
  },
  modalButtonSecondary: {
    backgroundColor: 'transparent',
    borderWidth: 1,
    borderColor: colors.neutral[300],
  },
  modalButtonText: {
    color: colors.neutral.white,
    fontSize: typography.fontSize.md,
    fontWeight: typography.fontWeight.semibold,
    textAlign: 'center',
  },
  modalButtonTextSecondary: {
    color: colors.neutral[700],
    fontSize: typography.fontSize.md,
    fontWeight: typography.fontWeight.semibold,
    textAlign: 'center',
  },
});
