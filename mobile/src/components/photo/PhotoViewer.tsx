/**
 * Просмотрщик фотографий с жестами
 */
import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  Modal,
  Image,
  TouchableOpacity,
  Dimensions,
  ScrollView,
} from 'react-native';
import { colors } from '../../theme/colors';
import { spacing } from '../../theme/spacing';
import { typography } from '../../theme/typography';
import { formatDateTime } from '../../utils/date';

const { width: SCREEN_WIDTH, height: SCREEN_HEIGHT } = Dimensions.get('window');

interface Photo {
  id: number;
  uri: string;
  latitude?: number;
  longitude?: number;
  takenAt: string;
  description?: string;
  hasDefects?: boolean;
  defectsCount?: number;
}

interface PhotoViewerProps {
  visible: boolean;
  photos: Photo[];
  currentIndex: number;
  onClose: () => void;
  onDelete?: (photo: Photo) => void;
  onShare?: (photo: Photo) => void;
}

export const PhotoViewer: React.FC<PhotoViewerProps> = ({
  visible,
  photos,
  currentIndex,
  onClose,
  onDelete,
  onShare,
}) => {
  const [index, setIndex] = useState(currentIndex);

  const currentPhoto = photos[index];

  const handlePrevious = () => {
    if (index > 0) {
      setIndex(index - 1);
    }
  };

  const handleNext = () => {
    if (index < photos.length - 1) {
      setIndex(index + 1);
    }
  };

  if (!currentPhoto) return null;

  return (
    <Modal
      visible={visible}
      transparent
      animationType="fade"
      onRequestClose={onClose}
    >
      <View style={styles.container}>
        {/* Header */}
        <View style={styles.header}>
          <TouchableOpacity style={styles.closeButton} onPress={onClose}>
            <Text style={styles.closeButtonText}>✕</Text>
          </TouchableOpacity>

          <View style={styles.counter}>
            <Text style={styles.counterText}>
              {index + 1} / {photos.length}
            </Text>
          </View>

          <View style={styles.headerActions}>
            {onShare && (
              <TouchableOpacity
                style={styles.actionButton}
                onPress={() => onShare(currentPhoto)}
              >
                <Text style={styles.actionButtonText}>📤</Text>
              </TouchableOpacity>
            )}
            {onDelete && (
              <TouchableOpacity
                style={styles.actionButton}
                onPress={() => onDelete(currentPhoto)}
              >
                <Text style={styles.actionButtonText}>🗑️</Text>
              </TouchableOpacity>
            )}
          </View>
        </View>

        {/* Photo */}
        <ScrollView
          contentContainerStyle={styles.imageContainer}
          maximumZoomScale={3}
          minimumZoomScale={1}
          showsHorizontalScrollIndicator={false}
          showsVerticalScrollIndicator={false}
        >
          <Image
            source={{ uri: currentPhoto.uri }}
            style={styles.image}
            resizeMode="contain"
          />
        </ScrollView>

        {/* Navigation */}
        <View style={styles.navigation}>
          <TouchableOpacity
            style={[styles.navButton, index === 0 && styles.navButtonDisabled]}
            onPress={handlePrevious}
            disabled={index === 0}
          >
            <Text style={styles.navButtonText}>‹</Text>
          </TouchableOpacity>

          <TouchableOpacity
            style={[
              styles.navButton,
              index === photos.length - 1 && styles.navButtonDisabled,
            ]}
            onPress={handleNext}
            disabled={index === photos.length - 1}
          >
            <Text style={styles.navButtonText}>›</Text>
          </TouchableOpacity>
        </View>

        {/* Info */}
        <View style={styles.info}>
          <View style={styles.infoRow}>
            <Text style={styles.infoLabel}>Дата:</Text>
            <Text style={styles.infoValue}>
              {formatDateTime(new Date(currentPhoto.takenAt))}
            </Text>
          </View>

          {currentPhoto.latitude && currentPhoto.longitude && (
            <View style={styles.infoRow}>
              <Text style={styles.infoLabel}>GPS:</Text>
              <Text style={styles.infoValue}>
                {currentPhoto.latitude.toFixed(6)}, {currentPhoto.longitude.toFixed(6)}
              </Text>
            </View>
          )}

          {currentPhoto.hasDefects && (
            <View style={styles.infoRow}>
              <Text style={styles.infoLabel}>Дефекты:</Text>
              <Text style={[styles.infoValue, styles.defectText]}>
                Обнаружено: {currentPhoto.defectsCount || 0}
              </Text>
            </View>
          )}

          {currentPhoto.description && (
            <View style={styles.descriptionContainer}>
              <Text style={styles.description}>{currentPhoto.description}</Text>
            </View>
          )}
        </View>
      </View>
    </Modal>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.neutral.black,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: spacing.md,
    paddingTop: spacing.xl,
    paddingBottom: spacing.md,
    backgroundColor: 'rgba(0, 0, 0, 0.8)',
  },
  closeButton: {
    width: 40,
    height: 40,
    justifyContent: 'center',
    alignItems: 'center',
  },
  closeButtonText: {
    color: colors.neutral.white,
    fontSize: typography.fontSize.xxl,
    fontWeight: typography.fontWeight.bold,
  },
  counter: {
    flex: 1,
    alignItems: 'center',
  },
  counterText: {
    color: colors.neutral.white,
    fontSize: typography.fontSize.md,
    fontWeight: typography.fontWeight.medium,
  },
  headerActions: {
    flexDirection: 'row',
    gap: spacing.sm,
  },
  actionButton: {
    width: 40,
    height: 40,
    justifyContent: 'center',
    alignItems: 'center',
  },
  actionButtonText: {
    fontSize: typography.fontSize.xl,
  },
  imageContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  image: {
    width: SCREEN_WIDTH,
    height: SCREEN_HEIGHT * 0.6,
  },
  navigation: {
    position: 'absolute',
    top: '50%',
    left: 0,
    right: 0,
    flexDirection: 'row',
    justifyContent: 'space-between',
    paddingHorizontal: spacing.md,
  },
  navButton: {
    width: 50,
    height: 50,
    borderRadius: spacing.borderRadius.full,
    backgroundColor: 'rgba(255, 255, 255, 0.3)',
    justifyContent: 'center',
    alignItems: 'center',
  },
  navButtonDisabled: {
    opacity: 0.3,
  },
  navButtonText: {
    color: colors.neutral.white,
    fontSize: typography.fontSize.xxxl,
    fontWeight: typography.fontWeight.bold,
  },
  info: {
    backgroundColor: 'rgba(0, 0, 0, 0.8)',
    paddingHorizontal: spacing.md,
    paddingVertical: spacing.lg,
  },
  infoRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: spacing.sm,
  },
  infoLabel: {
    color: colors.neutral[400],
    fontSize: typography.fontSize.sm,
  },
  infoValue: {
    color: colors.neutral.white,
    fontSize: typography.fontSize.sm,
    fontWeight: typography.fontWeight.medium,
  },
  defectText: {
    color: colors.error.light,
  },
  descriptionContainer: {
    marginTop: spacing.sm,
    paddingTop: spacing.sm,
    borderTopWidth: 1,
    borderTopColor: colors.neutral[700],
  },
  description: {
    color: colors.neutral.white,
    fontSize: typography.fontSize.md,
    lineHeight: typography.fontSize.md * typography.lineHeight.normal,
  },
});
