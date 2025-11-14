/**
 * Утилиты для работы с разрешениями
 */
import { Platform, PermissionsAndroid, Alert } from 'react-native';

export type PermissionType =
  | 'camera'
  | 'location'
  | 'storage'
  | 'microphone'
  | 'notifications';

export type PermissionStatus = 'granted' | 'denied' | 'never_ask_again';

/**
 * Проверка разрешения
 */
export async function checkPermission(
  type: PermissionType
): Promise<PermissionStatus> {
  if (Platform.OS === 'android') {
    try {
      const permission = getAndroidPermission(type);
      const result = await PermissionsAndroid.check(permission);
      return result ? 'granted' : 'denied';
    } catch (error) {
      console.error('Error checking permission:', error);
      return 'denied';
    }
  } else {
    // iOS - используйте react-native-permissions
    // import { check, PERMISSIONS } from 'react-native-permissions';
    // const permission = getIOSPermission(type);
    // const result = await check(permission);
    // return mapIOSPermissionStatus(result);
    return 'granted'; // Заглушка для iOS
  }
}

/**
 * Запрос разрешения
 */
export async function requestPermission(
  type: PermissionType
): Promise<PermissionStatus> {
  if (Platform.OS === 'android') {
    try {
      const permission = getAndroidPermission(type);
      const result = await PermissionsAndroid.request(permission, {
        title: getPermissionTitle(type),
        message: getPermissionMessage(type),
        buttonPositive: 'Разрешить',
        buttonNegative: 'Отмена',
      });

      switch (result) {
        case PermissionsAndroid.RESULTS.GRANTED:
          return 'granted';
        case PermissionsAndroid.RESULTS.NEVER_ASK_AGAIN:
          return 'never_ask_again';
        default:
          return 'denied';
      }
    } catch (error) {
      console.error('Error requesting permission:', error);
      return 'denied';
    }
  } else {
    // iOS - используйте react-native-permissions
    // import { request, PERMISSIONS } from 'react-native-permissions';
    // const permission = getIOSPermission(type);
    // const result = await request(permission);
    // return mapIOSPermissionStatus(result);
    return 'granted'; // Заглушка для iOS
  }
}

/**
 * Запрос разрешения с обработкой отказа
 */
export async function requestPermissionWithFallback(
  type: PermissionType
): Promise<boolean> {
  const status = await checkPermission(type);

  if (status === 'granted') {
    return true;
  }

  if (status === 'never_ask_again') {
    showSettingsAlert(type);
    return false;
  }

  const result = await requestPermission(type);

  if (result === 'granted') {
    return true;
  }

  if (result === 'never_ask_again') {
    showSettingsAlert(type);
  }

  return false;
}

/**
 * Запрос множественных разрешений
 */
export async function requestMultiplePermissions(
  types: PermissionType[]
): Promise<Record<PermissionType, PermissionStatus>> {
  const results: Record<string, PermissionStatus> = {};

  for (const type of types) {
    results[type] = await requestPermission(type);
  }

  return results as Record<PermissionType, PermissionStatus>;
}

/**
 * Получение Android разрешения
 */
function getAndroidPermission(type: PermissionType): string {
  switch (type) {
    case 'camera':
      return PermissionsAndroid.PERMISSIONS.CAMERA;
    case 'location':
      return PermissionsAndroid.PERMISSIONS.ACCESS_FINE_LOCATION;
    case 'storage':
      return PermissionsAndroid.PERMISSIONS.WRITE_EXTERNAL_STORAGE;
    case 'microphone':
      return PermissionsAndroid.PERMISSIONS.RECORD_AUDIO;
    case 'notifications':
      return PermissionsAndroid.PERMISSIONS.POST_NOTIFICATIONS;
    default:
      throw new Error(`Unknown permission type: ${type}`);
  }
}

/**
 * Заголовок для запроса разрешения
 */
function getPermissionTitle(type: PermissionType): string {
  switch (type) {
    case 'camera':
      return 'Разрешение на использование камеры';
    case 'location':
      return 'Разрешение на доступ к местоположению';
    case 'storage':
      return 'Разрешение на доступ к файлам';
    case 'microphone':
      return 'Разрешение на использование микрофона';
    case 'notifications':
      return 'Разрешение на отправку уведомлений';
    default:
      return 'Разрешение';
  }
}

/**
 * Сообщение для запроса разрешения
 */
function getPermissionMessage(type: PermissionType): string {
  switch (type) {
    case 'camera':
      return 'Для фотофиксации объектов строительства необходим доступ к камере.';
    case 'location':
      return 'Для привязки фотографий к местоположению необходим доступ к геолокации.';
    case 'storage':
      return 'Для сохранения фотографий и документов необходим доступ к файлам.';
    case 'microphone':
      return 'Для записи голосовых заметок необходим доступ к микрофону.';
    case 'notifications':
      return 'Для получения уведомлений о проверках необходимо разрешение.';
    default:
      return 'Приложению необходимо разрешение для корректной работы.';
  }
}

/**
 * Показать диалог с предложением перейти в настройки
 */
function showSettingsAlert(type: PermissionType): void {
  Alert.alert(
    'Разрешение отклонено',
    `Для использования функции необходимо разрешение. Перейдите в настройки приложения и разрешите доступ к ${getPermissionName(type)}.`,
    [
      {
        text: 'Отмена',
        style: 'cancel',
      },
      {
        text: 'Открыть настройки',
        onPress: () => {
          // Открытие настроек приложения
          // import { Linking } from 'react-native';
          // Linking.openSettings();
        },
      },
    ]
  );
}

/**
 * Получить название разрешения
 */
function getPermissionName(type: PermissionType): string {
  switch (type) {
    case 'camera':
      return 'камере';
    case 'location':
      return 'местоположению';
    case 'storage':
      return 'файлам';
    case 'microphone':
      return 'микрофону';
    case 'notifications':
      return 'уведомлениям';
    default:
      return 'функции';
  }
}
