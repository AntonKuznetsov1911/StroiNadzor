/**
 * Swipeable Row - строка списка с свайпом
 */
import React, { useRef } from 'react';
import {
  View,
  Text,
  StyleSheet,
  Animated,
  PanResponder,
  TouchableOpacity,
  Dimensions,
} from 'react-native';
import { colors } from '../../theme/colors';
import { spacing } from '../../theme/spacing';
import { typography } from '../../theme/typography';

const { width: SCREEN_WIDTH } = Dimensions.get('window');
const ACTION_WIDTH = 80;

export interface SwipeAction {
  text: string;
  icon?: string;
  color: string;
  onPress: () => void;
}

interface SwipeableRowProps {
  children: React.ReactNode;
  leftActions?: SwipeAction[];
  rightActions?: SwipeAction[];
  onSwipeStart?: () => void;
  onSwipeEnd?: () => void;
}

export const SwipeableRow: React.FC<SwipeableRowProps> = ({
  children,
  leftActions = [],
  rightActions = [],
  onSwipeStart,
  onSwipeEnd,
}) => {
  const translateX = useRef(new Animated.Value(0)).current;
  const maxLeftSwipe = leftActions.length * ACTION_WIDTH;
  const maxRightSwipe = rightActions.length * ACTION_WIDTH;

  const panResponder = useRef(
    PanResponder.create({
      onStartShouldSetPanResponder: () => true,
      onMoveShouldSetPanResponder: (_, gestureState) => {
        return Math.abs(gestureState.dx) > 5;
      },
      onPanResponderGrant: () => {
        onSwipeStart?.();
      },
      onPanResponderMove: (_, gestureState) => {
        const newValue = gestureState.dx;

        // Ограничиваем свайп
        if (newValue > 0 && leftActions.length > 0) {
          translateX.setValue(Math.min(newValue, maxLeftSwipe));
        } else if (newValue < 0 && rightActions.length > 0) {
          translateX.setValue(Math.max(newValue, -maxRightSwipe));
        }
      },
      onPanResponderRelease: (_, gestureState) => {
        const threshold = ACTION_WIDTH * 0.5;

        if (gestureState.dx > threshold && leftActions.length > 0) {
          // Открыть левые действия
          Animated.spring(translateX, {
            toValue: maxLeftSwipe,
            useNativeDriver: true,
          }).start();
        } else if (gestureState.dx < -threshold && rightActions.length > 0) {
          // Открыть правые действия
          Animated.spring(translateX, {
            toValue: -maxRightSwipe,
            useNativeDriver: true,
          }).start();
        } else {
          // Закрыть
          closeRow();
        }

        onSwipeEnd?.();
      },
    })
  ).current;

  const closeRow = () => {
    Animated.spring(translateX, {
      toValue: 0,
      useNativeDriver: true,
    }).start();
  };

  const handleActionPress = (action: SwipeAction) => {
    action.onPress();
    closeRow();
  };

  return (
    <View style={styles.container}>
      {/* Левые действия */}
      {leftActions.length > 0 && (
        <View style={styles.actionsLeft}>
          {leftActions.map((action, index) => (
            <TouchableOpacity
              key={index}
              style={[styles.action, { backgroundColor: action.color }]}
              onPress={() => handleActionPress(action)}
            >
              {action.icon && <Text style={styles.actionIcon}>{action.icon}</Text>}
              <Text style={styles.actionText}>{action.text}</Text>
            </TouchableOpacity>
          ))}
        </View>
      )}

      {/* Правые действия */}
      {rightActions.length > 0 && (
        <View style={styles.actionsRight}>
          {rightActions.map((action, index) => (
            <TouchableOpacity
              key={index}
              style={[styles.action, { backgroundColor: action.color }]}
              onPress={() => handleActionPress(action)}
            >
              {action.icon && <Text style={styles.actionIcon}>{action.icon}</Text>}
              <Text style={styles.actionText}>{action.text}</Text>
            </TouchableOpacity>
          ))}
        </View>
      )}

      {/* Контент */}
      <Animated.View
        style={[
          styles.content,
          {
            transform: [{ translateX }],
          },
        ]}
        {...panResponder.panHandlers}
      >
        {children}
      </Animated.View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    position: 'relative',
    overflow: 'hidden',
  },
  actionsLeft: {
    position: 'absolute',
    left: 0,
    top: 0,
    bottom: 0,
    flexDirection: 'row',
  },
  actionsRight: {
    position: 'absolute',
    right: 0,
    top: 0,
    bottom: 0,
    flexDirection: 'row',
  },
  action: {
    width: ACTION_WIDTH,
    justifyContent: 'center',
    alignItems: 'center',
    paddingHorizontal: spacing.sm,
  },
  actionIcon: {
    fontSize: typography.fontSize.xl,
    marginBottom: spacing.xs,
  },
  actionText: {
    color: colors.neutral.white,
    fontSize: typography.fontSize.xs,
    fontWeight: typography.fontWeight.semibold,
    textAlign: 'center',
  },
  content: {
    backgroundColor: colors.neutral.white,
  },
});
