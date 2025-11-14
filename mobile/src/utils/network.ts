/**
 * Утилиты для работы с сетью
 */
import { Platform } from 'react-native';

export type NetworkType =
  | 'wifi'
  | 'cellular'
  | 'bluetooth'
  | 'ethernet'
  | 'wimax'
  | 'vpn'
  | 'none'
  | 'unknown';

export interface NetworkState {
  isConnected: boolean;
  isInternetReachable: boolean;
  type: NetworkType;
  details?: {
    isConnectionExpensive?: boolean;
    cellularGeneration?: '2g' | '3g' | '4g' | '5g';
  };
}

/**
 * Получение состояния сети
 */
export async function getNetworkState(): Promise<NetworkState> {
  try {
    // В реальном приложении используйте @react-native-community/netinfo
    // import NetInfo from '@react-native-community/netinfo';
    // const state = await NetInfo.fetch();

    // return {
    //   isConnected: state.isConnected ?? false,
    //   isInternetReachable: state.isInternetReachable ?? false,
    //   type: state.type as NetworkType,
    //   details: {
    //     isConnectionExpensive: state.details?.isConnectionExpensive,
    //     cellularGeneration: state.details?.cellularGeneration,
    //   },
    // };

    // Заглушка
    return {
      isConnected: true,
      isInternetReachable: true,
      type: 'wifi',
    };
  } catch (error) {
    console.error('Error getting network state:', error);
    return {
      isConnected: false,
      isInternetReachable: false,
      type: 'none',
    };
  }
}

/**
 * Проверка наличия интернет-соединения
 */
export async function isConnected(): Promise<boolean> {
  const state = await getNetworkState();
  return state.isConnected && state.isInternetReachable;
}

/**
 * Проверка WiFi подключения
 */
export async function isWifiConnected(): Promise<boolean> {
  const state = await getNetworkState();
  return state.type === 'wifi' && state.isConnected;
}

/**
 * Проверка мобильного подключения
 */
export async function isCellularConnected(): Promise<boolean> {
  const state = await getNetworkState();
  return state.type === 'cellular' && state.isConnected;
}

/**
 * Проверка дорогого подключения (платный трафик)
 */
export async function isConnectionExpensive(): Promise<boolean> {
  const state = await getNetworkState();
  return state.details?.isConnectionExpensive ?? false;
}

/**
 * Подписка на изменения сети
 */
export function subscribeToNetworkChanges(
  callback: (state: NetworkState) => void
): () => void {
  // В реальном приложении используйте @react-native-community/netinfo
  // import NetInfo from '@react-native-community/netinfo';

  // const unsubscribe = NetInfo.addEventListener((state) => {
  //   callback({
  //     isConnected: state.isConnected ?? false,
  //     isInternetReachable: state.isInternetReachable ?? false,
  //     type: state.type as NetworkType,
  //     details: {
  //       isConnectionExpensive: state.details?.isConnectionExpensive,
  //       cellularGeneration: state.details?.cellularGeneration,
  //     },
  //   });
  // });

  // return unsubscribe;

  // Заглушка
  return () => {};
}

/**
 * Проверка доступности сервера
 */
export async function pingServer(url: string): Promise<boolean> {
  try {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 5000);

    const response = await fetch(url, {
      method: 'HEAD',
      signal: controller.signal,
    });

    clearTimeout(timeoutId);
    return response.ok;
  } catch (error) {
    console.error('Error pinging server:', error);
    return false;
  }
}

/**
 * Измерение скорости загрузки (примерно)
 */
export async function measureDownloadSpeed(
  testUrl: string = 'https://www.google.com/images/phd/px.gif'
): Promise<number> {
  try {
    const startTime = Date.now();
    const response = await fetch(testUrl);
    const blob = await response.blob();
    const endTime = Date.now();

    const durationSeconds = (endTime - startTime) / 1000;
    const fileSizeBytes = blob.size;
    const speedBps = fileSizeBytes / durationSeconds;
    const speedMbps = (speedBps * 8) / (1024 * 1024);

    return Math.round(speedMbps * 100) / 100;
  } catch (error) {
    console.error('Error measuring download speed:', error);
    return 0;
  }
}

/**
 * Получение качества соединения
 */
export function getConnectionQuality(speedMbps: number): string {
  if (speedMbps >= 10) return 'Отличное';
  if (speedMbps >= 5) return 'Хорошее';
  if (speedMbps >= 2) return 'Среднее';
  if (speedMbps >= 0.5) return 'Плохое';
  return 'Очень плохое';
}

/**
 * Ожидание подключения к сети
 */
export async function waitForConnection(
  timeoutMs: number = 30000
): Promise<boolean> {
  const startTime = Date.now();

  while (Date.now() - startTime < timeoutMs) {
    const connected = await isConnected();
    if (connected) {
      return true;
    }
    await sleep(1000);
  }

  return false;
}

/**
 * Проверка, можно ли загружать большие файлы
 */
export async function canDownloadLargeFiles(): Promise<boolean> {
  const state = await getNetworkState();

  // Разрешаем загрузку только по WiFi или недорогому подключению
  if (state.type === 'wifi') {
    return true;
  }

  if (state.details?.isConnectionExpensive === false) {
    return true;
  }

  return false;
}

/**
 * Получение рекомендованного качества для загрузки
 */
export async function getRecommendedQuality(): Promise<
  'high' | 'medium' | 'low'
> {
  const state = await getNetworkState();

  if (state.type === 'wifi') {
    return 'high';
  }

  if (state.type === 'cellular') {
    const generation = state.details?.cellularGeneration;
    if (generation === '5g' || generation === '4g') {
      return 'medium';
    }
  }

  return 'low';
}

/**
 * Вспомогательная функция задержки
 */
function sleep(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

/**
 * Retry функция с экспоненциальной задержкой
 */
export async function retryWithBackoff<T>(
  fn: () => Promise<T>,
  maxRetries: number = 3,
  initialDelayMs: number = 1000
): Promise<T> {
  let lastError: Error | null = null;

  for (let i = 0; i < maxRetries; i++) {
    try {
      return await fn();
    } catch (error) {
      lastError = error as Error;
      const delay = initialDelayMs * Math.pow(2, i);
      await sleep(delay);
    }
  }

  throw lastError || new Error('Max retries exceeded');
}

/**
 * Получение информации о типе сети для логирования
 */
export function getNetworkTypeDescription(type: NetworkType): string {
  const descriptions: Record<NetworkType, string> = {
    wifi: 'WiFi',
    cellular: 'Мобильная сеть',
    bluetooth: 'Bluetooth',
    ethernet: 'Ethernet',
    wimax: 'WiMAX',
    vpn: 'VPN',
    none: 'Нет подключения',
    unknown: 'Неизвестно',
  };

  return descriptions[type];
}
