/**
 * Hook для выбора изображений
 */
import { useState, useCallback } from 'react';
import { Alert } from 'react-native';
import { checkCameraPermissions } from '../utils/camera';

export interface ImagePickerOptions {
  allowsEditing?: boolean;
  quality?: number;
  aspect?: [number, number];
  allowsMultipleSelection?: boolean;
}

export interface PickedImage {
  uri: string;
  width: number;
  height: number;
  type?: string;
  fileName?: string;
  fileSize?: number;
}

export function useImagePicker() {
  const [loading, setLoading] = useState(false);

  /**
   * Выбор изображения из галереи
   */
  const pickFromGallery = useCallback(
    async (
      options: ImagePickerOptions = {}
    ): Promise<PickedImage | null> => {
      try {
        setLoading(true);

        // В реальном приложении используйте react-native-image-picker
        // import { launchImageLibrary } from 'react-native-image-picker';

        // const result = await launchImageLibrary({
        //   mediaType: 'photo',
        //   quality: options.quality || 0.8,
        //   selectionLimit: options.allowsMultipleSelection ? 0 : 1,
        // });

        // if (result.didCancel) {
        //   return null;
        // }

        // if (result.errorCode) {
        //   Alert.alert('Ошибка', result.errorMessage || 'Не удалось выбрать изображение');
        //   return null;
        // }

        // const asset = result.assets?.[0];
        // if (!asset) return null;

        // return {
        //   uri: asset.uri || '',
        //   width: asset.width || 0,
        //   height: asset.height || 0,
        //   type: asset.type,
        //   fileName: asset.fileName,
        //   fileSize: asset.fileSize,
        // };

        // Заглушка
        return null;
      } catch (error) {
        console.error('Error picking image from gallery:', error);
        Alert.alert('Ошибка', 'Не удалось выбрать изображение');
        return null;
      } finally {
        setLoading(false);
      }
    },
    []
  );

  /**
   * Съемка фото с камеры
   */
  const takePhoto = useCallback(
    async (
      options: ImagePickerOptions = {}
    ): Promise<PickedImage | null> => {
      try {
        // Проверка разрешений
        const hasPermission = await checkCameraPermissions();
        if (!hasPermission) {
          return null;
        }

        setLoading(true);

        // В реальном приложении используйте react-native-image-picker
        // import { launchCamera } from 'react-native-image-picker';

        // const result = await launchCamera({
        //   mediaType: 'photo',
        //   quality: options.quality || 0.8,
        //   saveToPhotos: true,
        // });

        // if (result.didCancel) {
        //   return null;
        // }

        // if (result.errorCode) {
        //   Alert.alert('Ошибка', result.errorMessage || 'Не удалось сделать фото');
        //   return null;
        // }

        // const asset = result.assets?.[0];
        // if (!asset) return null;

        // return {
        //   uri: asset.uri || '',
        //   width: asset.width || 0,
        //   height: asset.height || 0,
        //   type: asset.type,
        //   fileName: asset.fileName,
        //   fileSize: asset.fileSize,
        // };

        // Заглушка
        return null;
      } catch (error) {
        console.error('Error taking photo:', error);
        Alert.alert('Ошибка', 'Не удалось сделать фото');
        return null;
      } finally {
        setLoading(false);
      }
    },
    []
  );

  /**
   * Выбор изображения (камера или галерея)
   */
  const pickImage = useCallback(
    async (
      options: ImagePickerOptions = {}
    ): Promise<PickedImage | null> => {
      return new Promise((resolve) => {
        Alert.alert(
          'Выбор изображения',
          'Выберите источник изображения',
          [
            {
              text: 'Камера',
              onPress: async () => {
                const result = await takePhoto(options);
                resolve(result);
              },
            },
            {
              text: 'Галерея',
              onPress: async () => {
                const result = await pickFromGallery(options);
                resolve(result);
              },
            },
            {
              text: 'Отмена',
              style: 'cancel',
              onPress: () => resolve(null),
            },
          ]
        );
      });
    },
    [takePhoto, pickFromGallery]
  );

  return {
    pickFromGallery,
    takePhoto,
    pickImage,
    loading,
  };
}
