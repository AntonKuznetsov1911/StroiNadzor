/**
 * Утилиты для работы с геолокацией
 */
import { Platform, Alert } from 'react-native';
import { requestPermission } from './permissions';

export interface Coordinates {
  latitude: number;
  longitude: number;
  accuracy?: number;
  altitude?: number;
  heading?: number;
  speed?: number;
}

export interface LocationError {
  code: number;
  message: string;
}

/**
 * Получение текущей геолокации
 */
export async function getCurrentLocation(): Promise<Coordinates> {
  try {
    // Проверка разрешений
    const permission = await requestPermission('location');
    if (permission !== 'granted') {
      throw new Error('Location permission denied');
    }

    // В реальном приложении используйте @react-native-community/geolocation
    // import Geolocation from '@react-native-community/geolocation';

    return new Promise((resolve, reject) => {
      // Geolocation.getCurrentPosition(
      //   (position) => {
      //     resolve({
      //       latitude: position.coords.latitude,
      //       longitude: position.coords.longitude,
      //       accuracy: position.coords.accuracy,
      //       altitude: position.coords.altitude,
      //       heading: position.coords.heading,
      //       speed: position.coords.speed,
      //     });
      //   },
      //   (error) => {
      //     reject(error);
      //   },
      //   {
      //     enableHighAccuracy: true,
      //     timeout: 15000,
      //     maximumAge: 10000,
      //   }
      // );

      // Заглушка для демо
      resolve({
        latitude: 55.751244,
        longitude: 37.618423,
        accuracy: 10,
      });
    });
  } catch (error) {
    console.error('Error getting location:', error);
    throw error;
  }
}

/**
 * Наблюдение за изменением геолокации
 */
export function watchLocation(
  onLocationChange: (coordinates: Coordinates) => void,
  onError?: (error: LocationError) => void
): () => void {
  // В реальном приложении используйте @react-native-community/geolocation
  // import Geolocation from '@react-native-community/geolocation';

  // const watchId = Geolocation.watchPosition(
  //   (position) => {
  //     onLocationChange({
  //       latitude: position.coords.latitude,
  //       longitude: position.coords.longitude,
  //       accuracy: position.coords.accuracy,
  //       altitude: position.coords.altitude,
  //       heading: position.coords.heading,
  //       speed: position.coords.speed,
  //     });
  //   },
  //   (error) => {
  //     if (onError) {
  //       onError({
  //         code: error.code,
  //         message: error.message,
  //       });
  //     }
  //   },
  //   {
  //     enableHighAccuracy: true,
  //     distanceFilter: 10, // Минимальное изменение в метрах
  //     interval: 5000, // Android
  //     fastestInterval: 2000, // Android
  //   }
  // );

  // Возвращаем функцию для остановки наблюдения
  // return () => {
  //   Geolocation.clearWatch(watchId);
  // };

  // Заглушка
  return () => {};
}

/**
 * Проверка доступности GPS
 */
export async function isLocationEnabled(): Promise<boolean> {
  try {
    // В Android можно проверить через react-native-device-info
    // import DeviceInfo from 'react-native-device-info';
    // const isEnabled = await DeviceInfo.isLocationEnabled();
    // return isEnabled;

    // Заглушка
    return true;
  } catch (error) {
    console.error('Error checking location status:', error);
    return false;
  }
}

/**
 * Запрос включения GPS
 */
export function requestLocationEnable(): void {
  Alert.alert(
    'GPS отключен',
    'Для привязки фотографий к местоположению необходимо включить GPS.',
    [
      {
        text: 'Отмена',
        style: 'cancel',
      },
      {
        text: 'Настройки',
        onPress: () => {
          // Открытие настроек местоположения
          // import { Linking } from 'react-native';
          // if (Platform.OS === 'android') {
          //   Linking.sendIntent('android.settings.LOCATION_SOURCE_SETTINGS');
          // } else {
          //   Linking.openSettings();
          // }
        },
      },
    ]
  );
}

/**
 * Форматирование адреса из координат (геокодирование)
 */
export async function reverseGeocode(
  latitude: number,
  longitude: number
): Promise<string> {
  try {
    // В реальном приложении используйте геокодирование API
    // Например, Google Maps Geocoding API или Yandex Geocoding API

    // const response = await fetch(
    //   `https://maps.googleapis.com/maps/api/geocode/json?latlng=${latitude},${longitude}&key=YOUR_API_KEY&language=ru`
    // );
    // const data = await response.json();
    // if (data.results && data.results.length > 0) {
    //   return data.results[0].formatted_address;
    // }

    // Заглушка
    return `${latitude.toFixed(6)}, ${longitude.toFixed(6)}`;
  } catch (error) {
    console.error('Error reverse geocoding:', error);
    return `${latitude.toFixed(6)}, ${longitude.toFixed(6)}`;
  }
}

/**
 * Получение координат из адреса (прямое геокодирование)
 */
export async function geocode(address: string): Promise<Coordinates | null> {
  try {
    // В реальном приложении используйте геокодирование API

    // const response = await fetch(
    //   `https://maps.googleapis.com/maps/api/geocode/json?address=${encodeURIComponent(address)}&key=YOUR_API_KEY&language=ru`
    // );
    // const data = await response.json();
    // if (data.results && data.results.length > 0) {
    //   const location = data.results[0].geometry.location;
    //   return {
    //     latitude: location.lat,
    //     longitude: location.lng,
    //   };
    // }

    // Заглушка
    return null;
  } catch (error) {
    console.error('Error geocoding:', error);
    return null;
  }
}

/**
 * Проверка точности координат
 */
export function isAccuracyAcceptable(accuracy?: number): boolean {
  if (!accuracy) return false;
  return accuracy <= 50; // Точность до 50 метров считается приемлемой
}

/**
 * Получение названия направления по углу
 */
export function getDirectionName(heading?: number): string {
  if (heading === undefined || heading === null) return 'Неизвестно';

  const directions = [
    'Север',
    'Северо-Восток',
    'Восток',
    'Юго-Восток',
    'Юг',
    'Юго-Запад',
    'Запад',
    'Северо-Запад',
  ];

  const index = Math.round(heading / 45) % 8;
  return directions[index];
}
