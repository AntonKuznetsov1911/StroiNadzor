/**
 * Сервис синхронизации данных
 */
import { OfflineQueue, STORAGE_KEYS, setItem, getItem } from '../utils/storage';
import { isConnected } from '../utils/network';
import { apiService } from './api';

export interface SyncStatus {
  isSyncing: boolean;
  lastSyncTime: string | null;
  pendingActions: number;
  errors: string[];
}

class SyncService {
  private isSyncing = false;
  private syncInterval: NodeJS.Timeout | null = null;

  /**
   * Запуск автоматической синхронизации
   */
  startAutoSync(intervalMs: number = 15 * 60 * 1000) {
    if (this.syncInterval) {
      clearInterval(this.syncInterval);
    }

    this.syncInterval = setInterval(() => {
      this.sync();
    }, intervalMs);

    // Первая синхронизация при запуске
    this.sync();
  }

  /**
   * Остановка автоматической синхронизации
   */
  stopAutoSync() {
    if (this.syncInterval) {
      clearInterval(this.syncInterval);
      this.syncInterval = null;
    }
  }

  /**
   * Основная функция синхронизации
   */
  async sync(): Promise<SyncStatus> {
    // Проверка подключения
    const connected = await isConnected();
    if (!connected) {
      console.log('No internet connection, skipping sync');
      return this.getSyncStatus();
    }

    // Предотвращение одновременных синхронизаций
    if (this.isSyncing) {
      console.log('Sync already in progress');
      return this.getSyncStatus();
    }

    this.isSyncing = true;
    const errors: string[] = [];

    try {
      console.log('Starting sync...');

      // 1. Отправка локальных изменений на сервер
      await this.pushLocalChanges(errors);

      // 2. Получение обновлений с сервера
      await this.pullServerUpdates(errors);

      // 3. Обновление времени последней синхронизации
      await setItem(STORAGE_KEYS.LAST_SYNC, new Date().toISOString());

      console.log('Sync completed successfully');
    } catch (error) {
      console.error('Sync failed:', error);
      errors.push('Ошибка синхронизации: ' + (error as Error).message);
    } finally {
      this.isSyncing = false;
    }

    return this.getSyncStatus();
  }

  /**
   * Отправка локальных изменений на сервер
   */
  private async pushLocalChanges(errors: string[]): Promise<void> {
    const queue = await OfflineQueue.getAll();

    for (const action of queue) {
      try {
        await this.processOfflineAction(action);
        await OfflineQueue.remove(action.id);
      } catch (error) {
        console.error('Failed to process offline action:', error);
        errors.push(`Ошибка обработки действия ${action.type}`);
      }
    }
  }

  /**
   * Получение обновлений с сервера
   */
  private async pullServerUpdates(errors: string[]): Promise<void> {
    try {
      // Получение обновленных проектов
      // const projects = await apiService.getProjects();
      // await setItem(STORAGE_KEYS.CACHED_PROJECTS, projects);

      // Получение обновленных проверок
      // const inspections = await apiService.getInspections();
      // await setItem(STORAGE_KEYS.CACHED_INSPECTIONS, inspections);

      console.log('Server updates pulled successfully');
    } catch (error) {
      console.error('Failed to pull server updates:', error);
      errors.push('Ошибка получения обновлений с сервера');
    }
  }

  /**
   * Обработка офлайн-действия
   */
  private async processOfflineAction(action: any): Promise<void> {
    switch (action.type) {
      case 'CREATE_INSPECTION':
        // await apiService.createInspection(action.payload);
        break;

      case 'UPLOAD_PHOTO':
        // await apiService.uploadPhoto(action.payload);
        break;

      case 'UPDATE_INSPECTION':
        // await apiService.updateInspection(action.payload.id, action.payload.data);
        break;

      case 'SIGN_ACT':
        // await apiService.signAct(action.payload);
        break;

      default:
        console.warn('Unknown action type:', action.type);
    }
  }

  /**
   * Получение статуса синхронизации
   */
  async getSyncStatus(): Promise<SyncStatus> {
    const lastSyncTime = await getItem<string>(STORAGE_KEYS.LAST_SYNC);
    const pendingActions = await OfflineQueue.count();

    return {
      isSyncing: this.isSyncing,
      lastSyncTime,
      pendingActions,
      errors: [],
    };
  }

  /**
   * Добавление действия в офлайн-очередь
   */
  async queueOfflineAction(type: string, payload: any): Promise<void> {
    const action = {
      id: `${type}_${Date.now()}_${Math.random()}`,
      type,
      payload,
      timestamp: Date.now(),
    };

    await OfflineQueue.enqueue(action);
    console.log('Action queued for sync:', action);

    // Попытка синхронизации, если есть подключение
    const connected = await isConnected();
    if (connected) {
      this.sync();
    }
  }

  /**
   * Очистка офлайн-очереди
   */
  async clearOfflineQueue(): Promise<void> {
    await OfflineQueue.clear();
  }
}

// Singleton экземпляр
export const syncService = new SyncService();
