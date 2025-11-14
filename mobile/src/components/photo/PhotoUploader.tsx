/**
 * Компонент загрузки фотографий
 */
import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  Image,
  ActivityIndicator,
  Alert,
} from 'react-native';
import { colors } from '../../theme/colors';
import { spacing } from '../../theme/spacing';
import { typography } from '../../theme/typography';
import { ProgressBar } from '../construction/ProgressBar';
import { formatFileSize } from '../../utils/formatters';

interface UploadingPhoto {
  id: string;
  uri: string;
  progress: number;
  status: 'uploading' | 'success' | 'error';
  error?: string;
}

interface PhotoUploaderProps {
  photos: UploadingPhoto[];
  onRetry?: (photoId: string) => void;
  onCancel?: (photoId: string) => void;
  onRemove?: (photoId: string) => void;
}

export const PhotoUploader: React.FC<PhotoUploaderProps> = ({
  photos,
  onRetry,
  onCancel,
  onRemove,
}) => {
  if (photos.length === 0) return null;

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>Загрузка фотографий</Text>
        <Text style={styles.count}>
          {photos.filter((p) => p.status === 'success').length} / {photos.length}
        </Text>
      </View>

      {photos.map((photo) => (
        <PhotoUploadItem
          key={photo.id}
          photo={photo}
          onRetry={onRetry}
          onCancel={onCancel}
          onRemove={onRemove}
        />
      ))}
    </View>
  );
};

interface PhotoUploadItemProps {
  photo: UploadingPhoto;
  onRetry?: (photoId: string) => void;
  onCancel?: (photoId: string) => void;
  onRemove?: (photoId: string) => void;
}

const PhotoUploadItem: React.FC<PhotoUploadItemProps> = ({
  photo,
  onRetry,
  onCancel,
  onRemove,
}) => {
  const getStatusIcon = () => {
    switch (photo.status) {
      case 'uploading':
        return <ActivityIndicator size="small" color={colors.primary.main} />;
      case 'success':
        return <Text style={styles.statusIcon}>✓</Text>;
      case 'error':
        return <Text style={[styles.statusIcon, styles.errorIcon]}>✕</Text>;
    }
  };

  const getStatusText = () => {
    switch (photo.status) {
      case 'uploading':
        return `Загрузка... ${photo.progress}%`;
      case 'success':
        return 'Загружено';
      case 'error':
        return photo.error || 'Ошибка загрузки';
    }
  };

  return (
    <View style={styles.item}>
      <Image source={{ uri: photo.uri }} style={styles.thumbnail} />

      <View style={styles.itemContent}>
        <View style={styles.itemHeader}>
          <View style={styles.statusContainer}>
            {getStatusIcon()}
            <Text
              style={[
                styles.statusText,
                photo.status === 'error' && styles.errorText,
              ]}
            >
              {getStatusText()}
            </Text>
          </View>

          {photo.status === 'uploading' && onCancel && (
            <TouchableOpacity onPress={() => onCancel(photo.id)}>
              <Text style={styles.actionText}>Отменить</Text>
            </TouchableOpacity>
          )}

          {photo.status === 'error' && onRetry && (
            <TouchableOpacity onPress={() => onRetry(photo.id)}>
              <Text style={styles.actionText}>Повторить</Text>
            </TouchableOpacity>
          )}

          {photo.status === 'success' && onRemove && (
            <TouchableOpacity onPress={() => onRemove(photo.id)}>
              <Text style={styles.actionText}>Удалить</Text>
            </TouchableOpacity>
          )}
        </View>

        {photo.status === 'uploading' && (
          <ProgressBar
            progress={photo.progress}
            height={4}
            color={colors.primary.main}
          />
        )}
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    backgroundColor: colors.neutral.white,
    borderRadius: spacing.borderRadius.md,
    padding: spacing.md,
    marginBottom: spacing.md,
    elevation: 2,
    shadowColor: colors.neutral.black,
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: spacing.md,
  },
  title: {
    fontSize: typography.fontSize.lg,
    fontWeight: typography.fontWeight.semibold,
    color: colors.neutral[900],
  },
  count: {
    fontSize: typography.fontSize.md,
    color: colors.neutral[600],
  },
  item: {
    flexDirection: 'row',
    marginBottom: spacing.md,
  },
  thumbnail: {
    width: 60,
    height: 60,
    borderRadius: spacing.borderRadius.sm,
    marginRight: spacing.md,
    backgroundColor: colors.neutral[200],
  },
  itemContent: {
    flex: 1,
    justifyContent: 'center',
  },
  itemHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: spacing.sm,
  },
  statusContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    flex: 1,
  },
  statusIcon: {
    fontSize: typography.fontSize.lg,
    color: colors.success.main,
    marginRight: spacing.xs,
  },
  errorIcon: {
    color: colors.error.main,
  },
  statusText: {
    fontSize: typography.fontSize.sm,
    color: colors.neutral[700],
  },
  errorText: {
    color: colors.error.main,
  },
  actionText: {
    fontSize: typography.fontSize.sm,
    color: colors.primary.main,
    fontWeight: typography.fontWeight.medium,
  },
});
