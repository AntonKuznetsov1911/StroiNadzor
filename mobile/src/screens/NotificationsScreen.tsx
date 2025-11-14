/**
 * Экран уведомлений
 */
import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  FlatList,
  TouchableOpacity,
  RefreshControl,
} from 'react-native';
import { colors } from '../theme/colors';
import { spacing } from '../theme/spacing';
import { typography } from '../theme/typography';
import { EmptyState } from '../components/common/EmptyState';
import { formatDateTime } from '../utils/date';

interface Notification {
  id: number;
  title: string;
  message: string;
  type: 'inspection' | 'hidden_work' | 'defect' | 'document' | 'system';
  isRead: boolean;
  createdAt: string;
  relatedId?: number;
}

const MOCK_NOTIFICATIONS: Notification[] = [
  {
    id: 1,
    title: 'Новая проверка назначена',
    message: 'Вам назначена проверка на объекте "ЖК Солнечный" на 10.11.2025',
    type: 'inspection',
    isRead: false,
    createdAt: '2025-11-08T10:30:00',
    relatedId: 15,
  },
  {
    id: 2,
    title: 'Обнаружен критический дефект',
    message: 'ML-модель обнаружила критическую трещину в бетоне',
    type: 'defect',
    isRead: false,
    createdAt: '2025-11-08T09:15:00',
    relatedId: 42,
  },
  {
    id: 3,
    title: 'Скрытые работы требуют проверки',
    message: 'Подрядчик завершил армирование на 5 этаже',
    type: 'hidden_work',
    isRead: true,
    createdAt: '2025-11-07T16:45:00',
    relatedId: 28,
  },
  {
    id: 4,
    title: 'Акт подписан',
    message: 'Акт освидетельствования №АСВ-123 подписан всеми сторонами',
    type: 'document',
    isRead: true,
    createdAt: '2025-11-07T14:20:00',
  },
  {
    id: 5,
    title: 'Обновление приложения',
    message: 'Доступна новая версия приложения 1.1.0',
    type: 'system',
    isRead: true,
    createdAt: '2025-11-06T12:00:00',
  },
];

const NOTIFICATION_ICONS: Record<Notification['type'], string> = {
  inspection: '📋',
  hidden_work: '🔨',
  defect: '⚠️',
  document: '📄',
  system: '⚙️',
};

const NOTIFICATION_COLORS: Record<Notification['type'], string> = {
  inspection: colors.info.light,
  hidden_work: colors.accent.light,
  defect: colors.error.light,
  document: colors.success.light,
  system: colors.neutral[200],
};

export const NotificationsScreen: React.FC = () => {
  const [notifications, setNotifications] = useState<Notification[]>(
    MOCK_NOTIFICATIONS
  );
  const [refreshing, setRefreshing] = useState(false);

  const onRefresh = async () => {
    setRefreshing(true);
    // Загрузка уведомлений
    setTimeout(() => {
      setRefreshing(false);
    }, 1000);
  };

  const handleNotificationPress = (notification: Notification) => {
    // Отметить как прочитанное
    setNotifications((prev) =>
      prev.map((n) => (n.id === notification.id ? { ...n, isRead: true } : n))
    );

    // Навигация к связанному контенту
    if (notification.relatedId) {
      // navigation.navigate(...)
    }
  };

  const handleMarkAllAsRead = () => {
    setNotifications((prev) => prev.map((n) => ({ ...n, isRead: true })));
  };

  const unreadCount = notifications.filter((n) => !n.isRead).length;

  const renderNotification = ({ item }: { item: Notification }) => (
    <TouchableOpacity
      style={[
        styles.notificationItem,
        !item.isRead && styles.notificationItemUnread,
      ]}
      onPress={() => handleNotificationPress(item)}
      activeOpacity={0.7}
    >
      <View
        style={[
          styles.iconContainer,
          { backgroundColor: NOTIFICATION_COLORS[item.type] },
        ]}
      >
        <Text style={styles.icon}>{NOTIFICATION_ICONS[item.type]}</Text>
      </View>

      <View style={styles.notificationContent}>
        <View style={styles.notificationHeader}>
          <Text
            style={[
              styles.notificationTitle,
              !item.isRead && styles.notificationTitleUnread,
            ]}
            numberOfLines={1}
          >
            {item.title}
          </Text>
          {!item.isRead && <View style={styles.unreadDot} />}
        </View>

        <Text style={styles.notificationMessage} numberOfLines={2}>
          {item.message}
        </Text>

        <Text style={styles.notificationTime}>
          {formatDateTime(new Date(item.createdAt))}
        </Text>
      </View>
    </TouchableOpacity>
  );

  return (
    <View style={styles.container}>
      {unreadCount > 0 && (
        <View style={styles.header}>
          <Text style={styles.unreadCount}>
            Непрочитанных: {unreadCount}
          </Text>
          <TouchableOpacity onPress={handleMarkAllAsRead}>
            <Text style={styles.markAllButton}>Отметить все как прочитанные</Text>
          </TouchableOpacity>
        </View>
      )}

      <FlatList
        data={notifications}
        renderItem={renderNotification}
        keyExtractor={(item) => item.id.toString()}
        refreshControl={
          <RefreshControl
            refreshing={refreshing}
            onRefresh={onRefresh}
            tintColor={colors.primary.main}
          />
        }
        ListEmptyComponent={
          <EmptyState
            icon="🔔"
            title="Нет уведомлений"
            description="Здесь будут отображаться уведомления о проверках, дефектах и других событиях"
          />
        }
        contentContainerStyle={
          notifications.length === 0 && styles.emptyContainer
        }
      />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.neutral.white,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: spacing.md,
    backgroundColor: colors.primary.light,
    borderBottomWidth: 1,
    borderBottomColor: colors.neutral[200],
  },
  unreadCount: {
    fontSize: typography.fontSize.md,
    fontWeight: typography.fontWeight.semibold,
    color: colors.primary.dark,
  },
  markAllButton: {
    fontSize: typography.fontSize.sm,
    color: colors.primary.main,
    fontWeight: typography.fontWeight.medium,
  },
  notificationItem: {
    flexDirection: 'row',
    padding: spacing.md,
    borderBottomWidth: 1,
    borderBottomColor: colors.neutral[200],
    backgroundColor: colors.neutral.white,
  },
  notificationItemUnread: {
    backgroundColor: colors.neutral[50],
  },
  iconContainer: {
    width: 48,
    height: 48,
    borderRadius: spacing.borderRadius.full,
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: spacing.md,
  },
  icon: {
    fontSize: typography.fontSize.xl,
  },
  notificationContent: {
    flex: 1,
  },
  notificationHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: spacing.xs,
  },
  notificationTitle: {
    flex: 1,
    fontSize: typography.fontSize.md,
    fontWeight: typography.fontWeight.medium,
    color: colors.neutral[700],
  },
  notificationTitleUnread: {
    fontWeight: typography.fontWeight.bold,
    color: colors.neutral[900],
  },
  unreadDot: {
    width: 8,
    height: 8,
    borderRadius: spacing.borderRadius.full,
    backgroundColor: colors.primary.main,
    marginLeft: spacing.xs,
  },
  notificationMessage: {
    fontSize: typography.fontSize.sm,
    color: colors.neutral[600],
    lineHeight: typography.fontSize.sm * typography.lineHeight.normal,
    marginBottom: spacing.xs,
  },
  notificationTime: {
    fontSize: typography.fontSize.xs,
    color: colors.neutral[500],
  },
  emptyContainer: {
    flex: 1,
  },
});
