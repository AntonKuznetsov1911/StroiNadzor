/**
 * Утилиты для работы с локальным хранилищем (AsyncStorage)
 */

/**
 * Сохранение значения в хранилище
 */
export async function setItem(key: string, value: any): Promise<boolean> {
  try {
    // В реальном приложении используйте @react-native-async-storage/async-storage
    // import AsyncStorage from '@react-native-async-storage/async-storage';

    const jsonValue = JSON.stringify(value);
    // await AsyncStorage.setItem(key, jsonValue);
    return true;
  } catch (error) {
    console.error('Error saving to storage:', error);
    return false;
  }
}

/**
 * Получение значения из хранилища
 */
export async function getItem<T>(key: string): Promise<T | null> {
  try {
    // В реальном приложении используйте @react-native-async-storage/async-storage
    // import AsyncStorage from '@react-native-async-storage/async-storage';

    // const jsonValue = await AsyncStorage.getItem(key);
    // return jsonValue != null ? JSON.parse(jsonValue) : null;

    return null;
  } catch (error) {
    console.error('Error reading from storage:', error);
    return null;
  }
}

/**
 * Удаление значения из хранилища
 */
export async function removeItem(key: string): Promise<boolean> {
  try {
    // В реальном приложении используйте @react-native-async-storage/async-storage
    // import AsyncStorage from '@react-native-async-storage/async-storage';

    // await AsyncStorage.removeItem(key);
    return true;
  } catch (error) {
    console.error('Error removing from storage:', error);
    return false;
  }
}

/**
 * Очистка всего хранилища
 */
export async function clear(): Promise<boolean> {
  try {
    // В реальном приложении используйте @react-native-async-storage/async-storage
    // import AsyncStorage from '@react-native-async-storage/async-storage';

    // await AsyncStorage.clear();
    return true;
  } catch (error) {
    console.error('Error clearing storage:', error);
    return false;
  }
}

/**
 * Получение всех ключей
 */
export async function getAllKeys(): Promise<string[]> {
  try {
    // В реальном приложении используйте @react-native-async-storage/async-storage
    // import AsyncStorage from '@react-native-async-storage/async-storage';

    // const keys = await AsyncStorage.getAllKeys();
    // return keys;

    return [];
  } catch (error) {
    console.error('Error getting all keys:', error);
    return [];
  }
}

/**
 * Получение множественных значений
 */
export async function multiGet(
  keys: string[]
): Promise<Record<string, any>> {
  try {
    // В реальном приложении используйте @react-native-async-storage/async-storage
    // import AsyncStorage from '@react-native-async-storage/async-storage';

    // const values = await AsyncStorage.multiGet(keys);
    // const result: Record<string, any> = {};

    // for (const [key, value] of values) {
    //   if (value) {
    //     result[key] = JSON.parse(value);
    //   }
    // }

    // return result;

    return {};
  } catch (error) {
    console.error('Error getting multiple values:', error);
    return {};
  }
}

/**
 * Сохранение множественных значений
 */
export async function multiSet(
  items: Record<string, any>
): Promise<boolean> {
  try {
    // В реальном приложении используйте @react-native-async-storage/async-storage
    // import AsyncStorage from '@react-native-async-storage/async-storage';

    // const pairs: [string, string][] = Object.entries(items).map(
    //   ([key, value]) => [key, JSON.stringify(value)]
    // );

    // await AsyncStorage.multiSet(pairs);
    return true;
  } catch (error) {
    console.error('Error setting multiple values:', error);
    return false;
  }
}

/**
 * Удаление множественных значений
 */
export async function multiRemove(keys: string[]): Promise<boolean> {
  try {
    // В реальном приложении используйте @react-native-async-storage/async-storage
    // import AsyncStorage from '@react-native-async-storage/async-storage';

    // await AsyncStorage.multiRemove(keys);
    return true;
  } catch (error) {
    console.error('Error removing multiple values:', error);
    return false;
  }
}

// Константы для ключей хранилища
export const STORAGE_KEYS = {
  AUTH_TOKEN: '@auth:token',
  USER_DATA: '@user:data',
  THEME: '@app:theme',
  LANGUAGE: '@app:language',
  OFFLINE_QUEUE: '@sync:offline_queue',
  LAST_SYNC: '@sync:last_sync',
  CACHED_PROJECTS: '@cache:projects',
  CACHED_INSPECTIONS: '@cache:inspections',
  SETTINGS: '@app:settings',
  ONBOARDING_COMPLETED: '@app:onboarding_completed',
} as const;

/**
 * Утилиты для работы с кэшем
 */
export class Cache {
  private static TTL_DEFAULT = 5 * 60 * 1000; // 5 минут

  /**
   * Сохранение в кэш с TTL
   */
  static async set(
    key: string,
    value: any,
    ttl: number = Cache.TTL_DEFAULT
  ): Promise<boolean> {
    const cacheItem = {
      value,
      expiresAt: Date.now() + ttl,
    };
    return await setItem(key, cacheItem);
  }

  /**
   * Получение из кэша с проверкой TTL
   */
  static async get<T>(key: string): Promise<T | null> {
    const cacheItem = await getItem<{ value: T; expiresAt: number }>(key);

    if (!cacheItem) {
      return null;
    }

    if (Date.now() > cacheItem.expiresAt) {
      await removeItem(key);
      return null;
    }

    return cacheItem.value;
  }

  /**
   * Проверка, есть ли валидное значение в кэше
   */
  static async has(key: string): Promise<boolean> {
    const value = await Cache.get(key);
    return value !== null;
  }

  /**
   * Очистка устаревших элементов кэша
   */
  static async clearExpired(): Promise<number> {
    try {
      const keys = await getAllKeys();
      let clearedCount = 0;

      for (const key of keys) {
        const item = await getItem<{ expiresAt: number }>(key);
        if (item && item.expiresAt && Date.now() > item.expiresAt) {
          await removeItem(key);
          clearedCount++;
        }
      }

      return clearedCount;
    } catch (error) {
      console.error('Error clearing expired cache:', error);
      return 0;
    }
  }
}

/**
 * Утилиты для работы с офлайн-очередью
 */
export class OfflineQueue {
  /**
   * Добавление действия в очередь
   */
  static async enqueue(action: {
    id: string;
    type: string;
    payload: any;
    timestamp: number;
  }): Promise<boolean> {
    try {
      const queue = (await getItem<typeof action[]>(
        STORAGE_KEYS.OFFLINE_QUEUE
      )) || [];
      queue.push(action);
      return await setItem(STORAGE_KEYS.OFFLINE_QUEUE, queue);
    } catch (error) {
      console.error('Error enqueueing action:', error);
      return false;
    }
  }

  /**
   * Получение всей очереди
   */
  static async getAll(): Promise<any[]> {
    return (await getItem<any[]>(STORAGE_KEYS.OFFLINE_QUEUE)) || [];
  }

  /**
   * Удаление действия из очереди
   */
  static async remove(id: string): Promise<boolean> {
    try {
      const queue = await OfflineQueue.getAll();
      const filtered = queue.filter((action) => action.id !== id);
      return await setItem(STORAGE_KEYS.OFFLINE_QUEUE, filtered);
    } catch (error) {
      console.error('Error removing from queue:', error);
      return false;
    }
  }

  /**
   * Очистка всей очереди
   */
  static async clear(): Promise<boolean> {
    return await setItem(STORAGE_KEYS.OFFLINE_QUEUE, []);
  }

  /**
   * Получение количества элементов в очереди
   */
  static async count(): Promise<number> {
    const queue = await OfflineQueue.getAll();
    return queue.length;
  }
}
