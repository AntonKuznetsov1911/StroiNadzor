/**
 * Утилиты для работы с камерой
 */
import { Alert } from 'react-native';
import { requestPermission } from './permissions';

export interface PhotoMetadata {
  latitude?: number;
  longitude?: number;
  timestamp: string;
  deviceInfo?: {
    make?: string;
    model?: string;
    os?: string;
  };
}

export interface CapturedPhoto {
  uri: string;
  width: number;
  height: number;
  metadata: PhotoMetadata;
}

/**
 * Проверка и запрос разрешений камеры
 */
export async function checkCameraPermissions(): Promise<boolean> {
  try {
    const cameraStatus = await requestPermission('camera');
    const storageStatus = await requestPermission('storage');

    if (cameraStatus !== 'granted' || storageStatus !== 'granted') {
      Alert.alert(
        'Разрешения не предоставлены',
        'Для использования камеры необходимы разрешения на доступ к камере и хранилищу.',
        [{ text: 'OK' }]
      );
      return false;
    }

    return true;
  } catch (error) {
    console.error('Error checking camera permissions:', error);
    return false;
  }
}

/**
 * Получение метаданных устройства
 */
export function getDeviceMetadata(): PhotoMetadata['deviceInfo'] {
  // В реальном приложении используйте react-native-device-info
  // import DeviceInfo from 'react-native-device-info';

  return {
    make: 'Unknown', // DeviceInfo.getBrand()
    model: 'Unknown', // DeviceInfo.getModel()
    os: 'Unknown', // DeviceInfo.getSystemVersion()
  };
}

/**
 * Создание метаданных фото
 */
export function createPhotoMetadata(
  latitude?: number,
  longitude?: number
): PhotoMetadata {
  return {
    latitude,
    longitude,
    timestamp: new Date().toISOString(),
    deviceInfo: getDeviceMetadata(),
  };
}

/**
 * Валидация фото
 */
export interface PhotoValidationResult {
  isValid: boolean;
  errors: string[];
}

export function validatePhoto(photo: CapturedPhoto): PhotoValidationResult {
  const errors: string[] = [];

  // Проверка размера
  if (photo.width < 640 || photo.height < 480) {
    errors.push('Разрешение фото слишком низкое (минимум 640x480)');
  }

  // Проверка GPS координат
  if (!photo.metadata.latitude || !photo.metadata.longitude) {
    errors.push('Отсутствуют GPS координаты');
  }

  // Проверка временной метки
  if (!photo.metadata.timestamp) {
    errors.push('Отсутствует временная метка');
  }

  return {
    isValid: errors.length === 0,
    errors,
  };
}

/**
 * Получение размера фото в байтах
 */
export async function getPhotoSize(uri: string): Promise<number> {
  try {
    // В реальном приложении используйте react-native-fs
    // import RNFS from 'react-native-fs';
    // const stat = await RNFS.stat(uri);
    // return stat.size;
    return 0; // Заглушка
  } catch (error) {
    console.error('Error getting photo size:', error);
    return 0;
  }
}

/**
 * Сжатие фото
 */
export async function compressPhoto(
  uri: string,
  quality: number = 0.8
): Promise<string> {
  try {
    // В реальном приложении используйте react-native-image-resizer
    // import ImageResizer from 'react-native-image-resizer';
    // const result = await ImageResizer.createResizedImage(
    //   uri,
    //   1920,
    //   1080,
    //   'JPEG',
    //   quality * 100
    // );
    // return result.uri;
    return uri; // Заглушка
  } catch (error) {
    console.error('Error compressing photo:', error);
    return uri;
  }
}

/**
 * Генерация уникального имени файла
 */
export function generatePhotoFileName(projectId?: number): string {
  const timestamp = Date.now();
  const random = Math.random().toString(36).substring(2, 9);
  const prefix = projectId ? `project_${projectId}_` : '';
  return `${prefix}photo_${timestamp}_${random}.jpg`;
}

/**
 * Форматирование координат для отображения
 */
export function formatCoordinatesForDisplay(
  latitude: number,
  longitude: number
): string {
  const latDirection = latitude >= 0 ? 'N' : 'S';
  const lonDirection = longitude >= 0 ? 'E' : 'W';

  const latAbs = Math.abs(latitude).toFixed(6);
  const lonAbs = Math.abs(longitude).toFixed(6);

  return `${latAbs}°${latDirection}, ${lonAbs}°${lonDirection}`;
}

/**
 * Расчет расстояния между двумя точками (в метрах)
 */
export function calculateDistance(
  lat1: number,
  lon1: number,
  lat2: number,
  lon2: number
): number {
  const R = 6371e3; // Радиус Земли в метрах
  const φ1 = (lat1 * Math.PI) / 180;
  const φ2 = (lat2 * Math.PI) / 180;
  const Δφ = ((lat2 - lat1) * Math.PI) / 180;
  const Δλ = ((lon2 - lon1) * Math.PI) / 180;

  const a =
    Math.sin(Δφ / 2) * Math.sin(Δφ / 2) +
    Math.cos(φ1) * Math.cos(φ2) * Math.sin(Δλ / 2) * Math.sin(Δλ / 2);
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));

  return R * c;
}

/**
 * Проверка, находится ли координата в пределах проекта
 */
export function isWithinProjectBounds(
  latitude: number,
  longitude: number,
  projectCenter: { latitude: number; longitude: number },
  radiusMeters: number = 1000
): boolean {
  const distance = calculateDistance(
    latitude,
    longitude,
    projectCenter.latitude,
    projectCenter.longitude
  );

  return distance <= radiusMeters;
}
