/**
 * Skeleton - индикатор загрузки контента
 */
import React, { useEffect, useRef } from 'react';
import { View, StyleSheet, Animated, ViewStyle } from 'react-native';
import { colors } from '../../theme/colors';
import { spacing } from '../../theme/spacing';

interface SkeletonProps {
  width?: number | string;
  height?: number;
  borderRadius?: number;
  style?: ViewStyle;
}

export const Skeleton: React.FC<SkeletonProps> = ({
  width = '100%',
  height = 20,
  borderRadius = spacing.borderRadius.sm,
  style,
}) => {
  const opacity = useRef(new Animated.Value(0.3)).current;

  useEffect(() => {
    const animation = Animated.loop(
      Animated.sequence([
        Animated.timing(opacity, {
          toValue: 1,
          duration: 800,
          useNativeDriver: true,
        }),
        Animated.timing(opacity, {
          toValue: 0.3,
          duration: 800,
          useNativeDriver: true,
        }),
      ])
    );

    animation.start();

    return () => animation.stop();
  }, []);

  return (
    <Animated.View
      style={[
        styles.skeleton,
        {
          width,
          height,
          borderRadius,
          opacity,
        },
        style,
      ]}
    />
  );
};

// Готовые компоновки скелетонов
export const SkeletonCard: React.FC = () => (
  <View style={styles.card}>
    <Skeleton width="100%" height={200} borderRadius={spacing.borderRadius.md} />
    <View style={styles.cardContent}>
      <Skeleton width="70%" height={20} />
      <View style={styles.spacer} />
      <Skeleton width="100%" height={16} />
      <View style={styles.spacer} />
      <Skeleton width="40%" height={16} />
    </View>
  </View>
);

export const SkeletonList: React.FC<{ count?: number }> = ({ count = 5 }) => (
  <View>
    {Array.from({ length: count }).map((_, index) => (
      <View key={index} style={styles.listItem}>
        <Skeleton width={60} height={60} borderRadius={spacing.borderRadius.full} />
        <View style={styles.listItemContent}>
          <Skeleton width="70%" height={18} />
          <View style={styles.spacer} />
          <Skeleton width="50%" height={14} />
        </View>
      </View>
    ))}
  </View>
);

export const SkeletonText: React.FC<{ lines?: number }> = ({ lines = 3 }) => (
  <View>
    {Array.from({ length: lines }).map((_, index) => (
      <View key={index}>
        <Skeleton
          width={index === lines - 1 ? '60%' : '100%'}
          height={16}
        />
        {index < lines - 1 && <View style={styles.spacer} />}
      </View>
    ))}
  </View>
);

const styles = StyleSheet.create({
  skeleton: {
    backgroundColor: colors.neutral[300],
  },
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
  cardContent: {
    padding: spacing.md,
  },
  spacer: {
    height: spacing.sm,
  },
  listItem: {
    flexDirection: 'row',
    padding: spacing.md,
    borderBottomWidth: 1,
    borderBottomColor: colors.neutral[200],
  },
  listItemContent: {
    flex: 1,
    marginLeft: spacing.md,
    justifyContent: 'center',
  },
});
