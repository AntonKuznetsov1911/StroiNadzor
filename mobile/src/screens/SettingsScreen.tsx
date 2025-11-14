/**
 * Экран настроек
 */
import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  Switch,
  TouchableOpacity,
  Alert,
} from 'react-native';
import { colors } from '../theme/colors';
import { spacing } from '../theme/spacing';
import { typography } from '../theme/typography';
import { Card } from '../components/common/Card';
import { Button } from '../components/common/Button';

export const SettingsScreen: React.FC = () => {
  const [notifications, setNotifications] = useState(true);
  const [autoSync, setAutoSync] = useState(true);
  const [offlineMode, setOfflineMode] = useState(false);
  const [photoQuality, setPhotoQuality] = useState<'high' | 'medium' | 'low'>(
    'high'
  );

  const handleClearCache = () => {
    Alert.alert(
      'Очистка кэша',
      'Вы уверены, что хотите очистить кэш приложения?',
      [
        { text: 'Отмена', style: 'cancel' },
        {
          text: 'Очистить',
          style: 'destructive',
          onPress: async () => {
            // Очистка кэша
            Alert.alert('Успешно', 'Кэш очищен');
          },
        },
      ]
    );
  };

  const handleLogout = () => {
    Alert.alert('Выход', 'Вы уверены, что хотите выйти из аккаунта?', [
      { text: 'Отмена', style: 'cancel' },
      {
        text: 'Выйти',
        style: 'destructive',
        onPress: () => {
          // Logout logic
        },
      },
    ]);
  };

  return (
    <ScrollView style={styles.container}>
      <Card style={styles.section}>
        <Text style={styles.sectionTitle}>Общие настройки</Text>

        <View style={styles.settingItem}>
          <View style={styles.settingInfo}>
            <Text style={styles.settingLabel}>Уведомления</Text>
            <Text style={styles.settingDescription}>
              Получать push-уведомления о проверках
            </Text>
          </View>
          <Switch
            value={notifications}
            onValueChange={setNotifications}
            trackColor={{ false: colors.neutral[300], true: colors.primary.light }}
            thumbColor={notifications ? colors.primary.main : colors.neutral.white}
          />
        </View>

        <View style={styles.settingItem}>
          <View style={styles.settingInfo}>
            <Text style={styles.settingLabel}>Автосинхронизация</Text>
            <Text style={styles.settingDescription}>
              Автоматически синхронизировать данные
            </Text>
          </View>
          <Switch
            value={autoSync}
            onValueChange={setAutoSync}
            trackColor={{ false: colors.neutral[300], true: colors.primary.light }}
            thumbColor={autoSync ? colors.primary.main : colors.neutral.white}
          />
        </View>

        <View style={styles.settingItem}>
          <View style={styles.settingInfo}>
            <Text style={styles.settingLabel}>Офлайн-режим</Text>
            <Text style={styles.settingDescription}>
              Работать без подключения к интернету
            </Text>
          </View>
          <Switch
            value={offlineMode}
            onValueChange={setOfflineMode}
            trackColor={{ false: colors.neutral[300], true: colors.primary.light }}
            thumbColor={offlineMode ? colors.primary.main : colors.neutral.white}
          />
        </View>
      </Card>

      <Card style={styles.section}>
        <Text style={styles.sectionTitle}>Качество фото</Text>

        <TouchableOpacity
          style={styles.radioItem}
          onPress={() => setPhotoQuality('high')}
        >
          <View style={styles.radioButton}>
            {photoQuality === 'high' && <View style={styles.radioButtonInner} />}
          </View>
          <View style={styles.settingInfo}>
            <Text style={styles.settingLabel}>Высокое (1920x1080)</Text>
            <Text style={styles.settingDescription}>
              Лучшее качество, больше размер файла
            </Text>
          </View>
        </TouchableOpacity>

        <TouchableOpacity
          style={styles.radioItem}
          onPress={() => setPhotoQuality('medium')}
        >
          <View style={styles.radioButton}>
            {photoQuality === 'medium' && (
              <View style={styles.radioButtonInner} />
            )}
          </View>
          <View style={styles.settingInfo}>
            <Text style={styles.settingLabel}>Среднее (1280x720)</Text>
            <Text style={styles.settingDescription}>
              Баланс качества и размера
            </Text>
          </View>
        </TouchableOpacity>

        <TouchableOpacity
          style={styles.radioItem}
          onPress={() => setPhotoQuality('low')}
        >
          <View style={styles.radioButton}>
            {photoQuality === 'low' && <View style={styles.radioButtonInner} />}
          </View>
          <View style={styles.settingInfo}>
            <Text style={styles.settingLabel}>Низкое (640x480)</Text>
            <Text style={styles.settingDescription}>
              Минимальный размер файла
            </Text>
          </View>
        </TouchableOpacity>
      </Card>

      <Card style={styles.section}>
        <Text style={styles.sectionTitle}>Хранилище</Text>

        <View style={styles.storageInfo}>
          <Text style={styles.storageLabel}>Занято:</Text>
          <Text style={styles.storageValue}>245 МБ</Text>
        </View>

        <View style={styles.storageInfo}>
          <Text style={styles.storageLabel}>Фотографии:</Text>
          <Text style={styles.storageValue}>198 МБ</Text>
        </View>

        <View style={styles.storageInfo}>
          <Text style={styles.storageLabel}>Документы:</Text>
          <Text style={styles.storageValue}>42 МБ</Text>
        </View>

        <View style={styles.storageInfo}>
          <Text style={styles.storageLabel}>Кэш:</Text>
          <Text style={styles.storageValue}>5 МБ</Text>
        </View>

        <Button
          title="Очистить кэш"
          onPress={handleClearCache}
          variant="outline"
          style={styles.clearButton}
        />
      </Card>

      <Card style={styles.section}>
        <Text style={styles.sectionTitle}>О приложении</Text>

        <View style={styles.infoItem}>
          <Text style={styles.infoLabel}>Версия:</Text>
          <Text style={styles.infoValue}>1.0.0</Text>
        </View>

        <View style={styles.infoItem}>
          <Text style={styles.infoLabel}>Последнее обновление:</Text>
          <Text style={styles.infoValue}>08.11.2025</Text>
        </View>

        <TouchableOpacity style={styles.linkItem}>
          <Text style={styles.linkText}>Политика конфиденциальности</Text>
        </TouchableOpacity>

        <TouchableOpacity style={styles.linkItem}>
          <Text style={styles.linkText}>Условия использования</Text>
        </TouchableOpacity>

        <TouchableOpacity style={styles.linkItem}>
          <Text style={styles.linkText}>Техподдержка</Text>
        </TouchableOpacity>
      </Card>

      <Button
        title="Выйти из аккаунта"
        onPress={handleLogout}
        variant="danger"
        style={styles.logoutButton}
      />
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.neutral[100],
  },
  section: {
    margin: spacing.md,
  },
  sectionTitle: {
    fontSize: typography.fontSize.lg,
    fontWeight: typography.fontWeight.bold,
    color: colors.neutral[900],
    marginBottom: spacing.md,
  },
  settingItem: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingVertical: spacing.md,
    borderBottomWidth: 1,
    borderBottomColor: colors.neutral[200],
  },
  settingInfo: {
    flex: 1,
    marginRight: spacing.md,
  },
  settingLabel: {
    fontSize: typography.fontSize.md,
    fontWeight: typography.fontWeight.medium,
    color: colors.neutral[900],
    marginBottom: spacing.xs / 2,
  },
  settingDescription: {
    fontSize: typography.fontSize.sm,
    color: colors.neutral[600],
  },
  radioItem: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: spacing.md,
    borderBottomWidth: 1,
    borderBottomColor: colors.neutral[200],
  },
  radioButton: {
    width: 24,
    height: 24,
    borderRadius: spacing.borderRadius.full,
    borderWidth: 2,
    borderColor: colors.primary.main,
    marginRight: spacing.md,
    justifyContent: 'center',
    alignItems: 'center',
  },
  radioButtonInner: {
    width: 12,
    height: 12,
    borderRadius: spacing.borderRadius.full,
    backgroundColor: colors.primary.main,
  },
  storageInfo: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    paddingVertical: spacing.sm,
  },
  storageLabel: {
    fontSize: typography.fontSize.md,
    color: colors.neutral[700],
  },
  storageValue: {
    fontSize: typography.fontSize.md,
    fontWeight: typography.fontWeight.semibold,
    color: colors.neutral[900],
  },
  clearButton: {
    marginTop: spacing.md,
  },
  infoItem: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    paddingVertical: spacing.sm,
  },
  infoLabel: {
    fontSize: typography.fontSize.md,
    color: colors.neutral[700],
  },
  infoValue: {
    fontSize: typography.fontSize.md,
    color: colors.neutral[900],
  },
  linkItem: {
    paddingVertical: spacing.md,
    borderTopWidth: 1,
    borderTopColor: colors.neutral[200],
  },
  linkText: {
    fontSize: typography.fontSize.md,
    color: colors.primary.main,
  },
  logoutButton: {
    margin: spacing.md,
    marginTop: spacing.lg,
    marginBottom: spacing.xl,
  },
});
