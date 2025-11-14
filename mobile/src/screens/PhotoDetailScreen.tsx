/**
 * Экран детальной информации о фото
 */
import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  Image,
  ScrollView,
  TouchableOpacity,
  Alert,
} from 'react-native';
import { colors } from '../theme/colors';
import { spacing } from '../theme/spacing';
import { typography } from '../theme/typography';
import { Card } from '../components/common/Card';
import { Button } from '../components/common/Button';
import { StatusBadge } from '../components/construction/StatusBadge';
import { formatDateTime } from '../utils/date';

export const PhotoDetailScreen: React.FC = () => {
  const [photo] = useState({
    id: 1,
    uri: 'https://example.com/photo.jpg',
    latitude: 55.751244,
    longitude: 37.618423,
    takenAt: '2025-11-08T10:30:00',
    description: 'Проверка качества бетонирования 5 этажа',
    hasDefects: true,
    defects: [
      {
        id: 1,
        type: 'crack',
        severity: 'major',
        confidence: 0.92,
        description: 'Трещина в бетоне, ширина ~2мм',
      },
      {
        id: 2,
        type: 'deviation',
        severity: 'minor',
        confidence: 0.85,
        description: 'Незначительное отклонение от вертикали',
      },
    ],
    metadata: {
      device: 'Samsung Galaxy S21',
      os: 'Android 13',
      fileSize: 2547891,
      resolution: '4000x3000',
    },
  });

  const handleDelete = () => {
    Alert.alert(
      'Удалить фото?',
      'Это действие нельзя будет отменить',
      [
        { text: 'Отмена', style: 'cancel' },
        {
          text: 'Удалить',
          style: 'destructive',
          onPress: () => {
            // Удаление фото
          },
        },
      ]
    );
  };

  const handleShare = () => {
    // Поделиться фото
  };

  const handleEdit = () => {
    // Редактировать описание
  };

  return (
    <ScrollView style={styles.container}>
      {/* Фото */}
      <Image source={{ uri: photo.uri }} style={styles.image} />

      {/* Информация */}
      <Card style={styles.infoCard}>
        <View style={styles.infoRow}>
          <Text style={styles.infoLabel}>Дата и время:</Text>
          <Text style={styles.infoValue}>
            {formatDateTime(new Date(photo.takenAt))}
          </Text>
        </View>

        <View style={styles.infoRow}>
          <Text style={styles.infoLabel}>Координаты:</Text>
          <TouchableOpacity>
            <Text style={[styles.infoValue, styles.link]}>
              {photo.latitude.toFixed(6)}, {photo.longitude.toFixed(6)}
            </Text>
          </TouchableOpacity>
        </View>

        <View style={styles.infoRow}>
          <Text style={styles.infoLabel}>Размер:</Text>
          <Text style={styles.infoValue}>
            {(photo.metadata.fileSize / 1024 / 1024).toFixed(2)} МБ
          </Text>
        </View>

        <View style={styles.infoRow}>
          <Text style={styles.infoLabel}>Разрешение:</Text>
          <Text style={styles.infoValue}>{photo.metadata.resolution}</Text>
        </View>

        <View style={styles.infoRow}>
          <Text style={styles.infoLabel}>Устройство:</Text>
          <Text style={styles.infoValue}>{photo.metadata.device}</Text>
        </View>
      </Card>

      {/* Описание */}
      <Card style={styles.descriptionCard}>
        <View style={styles.descriptionHeader}>
          <Text style={styles.sectionTitle}>Описание</Text>
          <TouchableOpacity onPress={handleEdit}>
            <Text style={styles.editButton}>Изменить</Text>
          </TouchableOpacity>
        </View>
        <Text style={styles.description}>{photo.description}</Text>
      </Card>

      {/* Дефекты */}
      {photo.hasDefects && (
        <Card style={styles.defectsCard}>
          <Text style={styles.sectionTitle}>
            Обнаруженные дефекты ({photo.defects.length})
          </Text>

          {photo.defects.map((defect) => (
            <View key={defect.id} style={styles.defectItem}>
              <View style={styles.defectHeader}>
                <Text style={styles.defectType}>{defect.type}</Text>
                <StatusBadge
                  status={
                    defect.severity === 'major'
                      ? 'warning'
                      : defect.severity === 'critical'
                      ? 'error'
                      : 'info'
                  }
                  label={defect.severity}
                  size="small"
                />
              </View>

              <Text style={styles.defectDescription}>
                {defect.description}
              </Text>

              <Text style={styles.defectConfidence}>
                Уверенность: {Math.round(defect.confidence * 100)}%
              </Text>
            </View>
          ))}
        </Card>
      )}

      {/* Действия */}
      <View style={styles.actions}>
        <Button
          title="Поделиться"
          onPress={handleShare}
          variant="outline"
          style={styles.actionButton}
        />
        <Button
          title="Удалить"
          onPress={handleDelete}
          variant="danger"
          style={styles.actionButton}
        />
      </View>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.neutral[100],
  },
  image: {
    width: '100%',
    height: 300,
    backgroundColor: colors.neutral[200],
  },
  infoCard: {
    margin: spacing.md,
  },
  infoRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    paddingVertical: spacing.sm,
    borderBottomWidth: 1,
    borderBottomColor: colors.neutral[200],
  },
  infoLabel: {
    fontSize: typography.fontSize.md,
    color: colors.neutral[600],
  },
  infoValue: {
    fontSize: typography.fontSize.md,
    fontWeight: typography.fontWeight.medium,
    color: colors.neutral[900],
  },
  link: {
    color: colors.primary.main,
  },
  descriptionCard: {
    margin: spacing.md,
    marginTop: 0,
  },
  descriptionHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: spacing.sm,
  },
  sectionTitle: {
    fontSize: typography.fontSize.lg,
    fontWeight: typography.fontWeight.bold,
    color: colors.neutral[900],
  },
  editButton: {
    fontSize: typography.fontSize.md,
    color: colors.primary.main,
    fontWeight: typography.fontWeight.medium,
  },
  description: {
    fontSize: typography.fontSize.md,
    color: colors.neutral[700],
    lineHeight: typography.fontSize.md * typography.lineHeight.normal,
  },
  defectsCard: {
    margin: spacing.md,
    marginTop: 0,
  },
  defectItem: {
    paddingTop: spacing.md,
    marginTop: spacing.md,
    borderTopWidth: 1,
    borderTopColor: colors.neutral[200],
  },
  defectHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: spacing.sm,
  },
  defectType: {
    fontSize: typography.fontSize.md,
    fontWeight: typography.fontWeight.semibold,
    color: colors.neutral[900],
  },
  defectDescription: {
    fontSize: typography.fontSize.md,
    color: colors.neutral[700],
    marginBottom: spacing.sm,
  },
  defectConfidence: {
    fontSize: typography.fontSize.sm,
    color: colors.neutral[500],
  },
  actions: {
    flexDirection: 'row',
    padding: spacing.md,
    gap: spacing.md,
  },
  actionButton: {
    flex: 1,
  },
});
