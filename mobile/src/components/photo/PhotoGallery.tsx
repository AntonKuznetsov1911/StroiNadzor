/**
 * Галерея фотографий
 */
import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  FlatList,
  TouchableOpacity,
  Image,
  Dimensions,
} from 'react-native';
import { colors } from '../../theme/colors';
import { spacing } from '../../theme/spacing';
import { typography } from '../../theme/typography';

const { width: SCREEN_WIDTH } = Dimensions.get('window');
const COLUMN_COUNT = 3;
const IMAGE_SIZE = (SCREEN_WIDTH - spacing.md * 4) / COLUMN_COUNT;

interface Photo {
  id: number;
  uri: string;
  thumbnail?: string;
  latitude?: number;
  longitude?: number;
  takenAt: string;
  hasDefects?: boolean;
}

interface PhotoGalleryProps {
  photos: Photo[];
  onPhotoPress?: (photo: Photo) => void;
  onPhotoLongPress?: (photo: Photo) => void;
  selectedPhotos?: number[];
  selectionMode?: boolean;
  onSelectionChange?: (selectedIds: number[]) => void;
}

export const PhotoGallery: React.FC<PhotoGalleryProps> = ({
  photos,
  onPhotoPress,
  onPhotoLongPress,
  selectedPhotos = [],
  selectionMode = false,
  onSelectionChange,
}) => {
  const [selected, setSelected] = useState<number[]>(selectedPhotos);

  const handlePhotoPress = (photo: Photo) => {
    if (selectionMode) {
      const newSelected = selected.includes(photo.id)
        ? selected.filter((id) => id !== photo.id)
        : [...selected, photo.id];

      setSelected(newSelected);
      onSelectionChange?.(newSelected);
    } else {
      onPhotoPress?.(photo);
    }
  };

  const handlePhotoLongPress = (photo: Photo) => {
    onPhotoLongPress?.(photo);
  };

  const renderPhoto = ({ item }: { item: Photo }) => {
    const isSelected = selected.includes(item.id);

    return (
      <TouchableOpacity
        style={[styles.photoContainer, isSelected && styles.photoSelected]}
        onPress={() => handlePhotoPress(item)}
        onLongPress={() => handlePhotoLongPress(item)}
        activeOpacity={0.7}
      >
        <Image
          source={{ uri: item.thumbnail || item.uri }}
          style={styles.photo}
          resizeMode="cover"
        />

        {item.hasDefects && (
          <View style={styles.defectBadge}>
            <Text style={styles.defectBadgeText}>⚠️</Text>
          </View>
        )}

        {isSelected && (
          <View style={styles.selectionOverlay}>
            <View style={styles.checkmark}>
              <Text style={styles.checkmarkText}>✓</Text>
            </View>
          </View>
        )}

        {item.latitude && item.longitude && (
          <View style={styles.gpsIndicator}>
            <Text style={styles.gpsIndicatorText}>📍</Text>
          </View>
        )}
      </TouchableOpacity>
    );
  };

  return (
    <FlatList
      data={photos}
      renderItem={renderPhoto}
      keyExtractor={(item) => item.id.toString()}
      numColumns={COLUMN_COUNT}
      contentContainerStyle={styles.container}
      showsVerticalScrollIndicator={false}
    />
  );
};

const styles = StyleSheet.create({
  container: {
    padding: spacing.sm,
  },
  photoContainer: {
    width: IMAGE_SIZE,
    height: IMAGE_SIZE,
    margin: spacing.xs / 2,
    borderRadius: spacing.borderRadius.sm,
    overflow: 'hidden',
    backgroundColor: colors.neutral[200],
  },
  photoSelected: {
    borderWidth: 3,
    borderColor: colors.primary.main,
  },
  photo: {
    width: '100%',
    height: '100%',
  },
  defectBadge: {
    position: 'absolute',
    top: spacing.xs,
    right: spacing.xs,
    backgroundColor: colors.error.main,
    borderRadius: spacing.borderRadius.full,
    width: 24,
    height: 24,
    justifyContent: 'center',
    alignItems: 'center',
  },
  defectBadgeText: {
    fontSize: typography.fontSize.sm,
  },
  gpsIndicator: {
    position: 'absolute',
    bottom: spacing.xs,
    left: spacing.xs,
    backgroundColor: 'rgba(0, 0, 0, 0.6)',
    borderRadius: spacing.borderRadius.sm,
    paddingHorizontal: spacing.xs,
    paddingVertical: spacing.xs / 2,
  },
  gpsIndicatorText: {
    fontSize: typography.fontSize.xs,
  },
  selectionOverlay: {
    ...StyleSheet.absoluteFillObject,
    backgroundColor: 'rgba(0, 0, 0, 0.3)',
    justifyContent: 'center',
    alignItems: 'center',
  },
  checkmark: {
    width: 32,
    height: 32,
    borderRadius: spacing.borderRadius.full,
    backgroundColor: colors.primary.main,
    justifyContent: 'center',
    alignItems: 'center',
  },
  checkmarkText: {
    color: colors.neutral.white,
    fontSize: typography.fontSize.lg,
    fontWeight: typography.fontWeight.bold,
  },
});
