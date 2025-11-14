/**
 * Выпадающий список (Dropdown)
 */
import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  Modal,
  FlatList,
  ScrollView,
} from 'react-native';
import { colors } from '../../theme/colors';
import { spacing } from '../../theme/spacing';
import { typography } from '../../theme/typography';

export interface DropdownOption {
  label: string;
  value: string | number;
}

interface DropdownProps {
  label?: string;
  value?: string | number;
  options: DropdownOption[];
  onChange: (value: string | number) => void;
  placeholder?: string;
  required?: boolean;
  error?: string;
  disabled?: boolean;
  searchable?: boolean;
}

export const Dropdown: React.FC<DropdownProps> = ({
  label,
  value,
  options,
  onChange,
  placeholder = 'Выберите значение',
  required = false,
  error,
  disabled = false,
  searchable = false,
}) => {
  const [isVisible, setIsVisible] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');

  const selectedOption = options.find((opt) => opt.value === value);

  const filteredOptions = searchQuery
    ? options.filter((opt) =>
        opt.label.toLowerCase().includes(searchQuery.toLowerCase())
      )
    : options;

  const handleSelect = (optionValue: string | number) => {
    onChange(optionValue);
    setIsVisible(false);
    setSearchQuery('');
  };

  const handlePress = () => {
    if (!disabled) {
      setIsVisible(true);
    }
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
            !selectedOption && styles.placeholder,
            disabled && styles.textDisabled,
          ]}
        >
          {selectedOption ? selectedOption.label : placeholder}
        </Text>
        <Text style={styles.icon}>{isVisible ? '▲' : '▼'}</Text>
      </TouchableOpacity>

      {error && <Text style={styles.error}>{error}</Text>}

      <Modal visible={isVisible} transparent animationType="fade">
        <TouchableOpacity
          style={styles.modalOverlay}
          activeOpacity={1}
          onPress={() => setIsVisible(false)}
        >
          <View
            style={styles.modalContent}
            onStartShouldSetResponder={() => true}
          >
            <View style={styles.modalHeader}>
              <Text style={styles.modalTitle}>
                {label || 'Выберите значение'}
              </Text>
              <TouchableOpacity onPress={() => setIsVisible(false)}>
                <Text style={styles.closeButton}>✕</Text>
              </TouchableOpacity>
            </View>

            <ScrollView style={styles.optionsList}>
              {filteredOptions.map((option) => (
                <TouchableOpacity
                  key={option.value}
                  style={[
                    styles.option,
                    option.value === value && styles.optionSelected,
                  ]}
                  onPress={() => handleSelect(option.value)}
                >
                  <Text
                    style={[
                      styles.optionText,
                      option.value === value && styles.optionTextSelected,
                    ]}
                  >
                    {option.label}
                  </Text>
                  {option.value === value && (
                    <Text style={styles.checkmark}>✓</Text>
                  )}
                </TouchableOpacity>
              ))}
            </ScrollView>
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
    fontSize: typography.fontSize.sm,
    color: colors.neutral[600],
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
    width: '80%',
    maxWidth: 400,
    maxHeight: '60%',
  },
  modalHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: spacing.md,
    borderBottomWidth: 1,
    borderBottomColor: colors.neutral[200],
  },
  modalTitle: {
    fontSize: typography.fontSize.lg,
    fontWeight: typography.fontWeight.semibold,
    color: colors.neutral[900],
  },
  closeButton: {
    fontSize: typography.fontSize.xl,
    color: colors.neutral[600],
    padding: spacing.xs,
  },
  optionsList: {
    maxHeight: 300,
  },
  option: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: spacing.md,
    borderBottomWidth: 1,
    borderBottomColor: colors.neutral[100],
  },
  optionSelected: {
    backgroundColor: colors.primary.light,
  },
  optionText: {
    fontSize: typography.fontSize.md,
    color: colors.neutral[900],
  },
  optionTextSelected: {
    color: colors.primary.main,
    fontWeight: typography.fontWeight.semibold,
  },
  checkmark: {
    fontSize: typography.fontSize.lg,
    color: colors.primary.main,
    fontWeight: typography.fontWeight.bold,
  },
});
