/**
 * Toast - всплывающее уведомление
 */
import React, { useEffect, useRef } from 'react';
import {
  View,
  Text,
  StyleSheet,
  Animated,
  TouchableOpacity,
  Dimensions,
} from 'react-native';
import { colors } from '../../theme/colors';
import { spacing } from '../../theme/spacing';
import { typography } from '../../theme/typography';

const { width: SCREEN_WIDTH } = Dimensions.get('window');

type ToastType = 'success' | 'error' | 'info' | 'warning';

interface ToastProps {
  visible: boolean;
  message: string;
  type?: ToastType;
  duration?: number;
  onDismiss?: () => void;
}

const TOAST_CONFIG: Record<ToastType, { icon: string; color: string }> = {
  success: { icon: '✓', color: colors.success.main },
  error: { icon: '✕', color: colors.error.main },
  info: { icon: 'ℹ', color: colors.info.main },
  warning: { icon: '⚠', color: colors.warning.main },
};

export const Toast: React.FC<ToastProps> = ({
  visible,
  message,
  type = 'info',
  duration = 3000,
  onDismiss,
}) => {
  const translateY = useRef(new Animated.Value(-100)).current;
  const opacity = useRef(new Animated.Value(0)).current;

  useEffect(() => {
    if (visible) {
      // Показать
      Animated.parallel([
        Animated.timing(translateY, {
          toValue: 0,
          duration: 300,
          useNativeDriver: true,
        }),
        Animated.timing(opacity, {
          toValue: 1,
          duration: 300,
          useNativeDriver: true,
        }),
      ]).start();

      // Автоскрытие
      const timer = setTimeout(() => {
        handleDismiss();
      }, duration);

      return () => clearTimeout(timer);
    }
  }, [visible]);

  const handleDismiss = () => {
    Animated.parallel([
      Animated.timing(translateY, {
        toValue: -100,
        duration: 250,
        useNativeDriver: true,
      }),
      Animated.timing(opacity, {
        toValue: 0,
        duration: 250,
        useNativeDriver: true,
      }),
    ]).start(() => {
      onDismiss?.();
    });
  };

  if (!visible) return null;

  const config = TOAST_CONFIG[type];

  return (
    <Animated.View
      style={[
        styles.container,
        {
          transform: [{ translateY }],
          opacity,
        },
      ]}
    >
      <TouchableOpacity
        style={[styles.toast, { borderLeftColor: config.color }]}
        onPress={handleDismiss}
        activeOpacity={0.9}
      >
        <View style={[styles.iconContainer, { backgroundColor: config.color }]}>
          <Text style={styles.icon}>{config.icon}</Text>
        </View>

        <Text style={styles.message} numberOfLines={2}>
          {message}
        </Text>

        <TouchableOpacity style={styles.closeButton} onPress={handleDismiss}>
          <Text style={styles.closeButtonText}>✕</Text>
        </TouchableOpacity>
      </TouchableOpacity>
    </Animated.View>
  );
};

const styles = StyleSheet.create({
  container: {
    position: 'absolute',
    top: spacing.xl,
    left: spacing.md,
    right: spacing.md,
    zIndex: 9999,
  },
  toast: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: colors.neutral.white,
    borderRadius: spacing.borderRadius.md,
    borderLeftWidth: 4,
    paddingVertical: spacing.md,
    paddingHorizontal: spacing.md,
    elevation: 8,
    shadowColor: colors.neutral.black,
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 8,
  },
  iconContainer: {
    width: 32,
    height: 32,
    borderRadius: spacing.borderRadius.full,
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: spacing.sm,
  },
  icon: {
    color: colors.neutral.white,
    fontSize: typography.fontSize.lg,
    fontWeight: typography.fontWeight.bold,
  },
  message: {
    flex: 1,
    fontSize: typography.fontSize.md,
    color: colors.neutral[900],
    lineHeight: typography.fontSize.md * typography.lineHeight.normal,
  },
  closeButton: {
    padding: spacing.xs,
    marginLeft: spacing.sm,
  },
  closeButtonText: {
    fontSize: typography.fontSize.lg,
    color: colors.neutral[500],
  },
});
