/**
 * Сервис офлайн-режима
 */
import { getItem, setItem, STORAGE_KEYS } from '../utils/storage';
import { isConnected } from '../utils/network';
import { Project, Inspection, HiddenWork } from '../types';

class OfflineService {
  /**
   * Кэширование проектов
   */
  async cacheProjects(projects: Project[]): Promise<void> {
    await setItem(STORAGE_KEYS.CACHED_PROJECTS, {
      data: projects,
      cachedAt: new Date().toISOString(),
    });
  }

  /**
   * Получение кэшированных проектов
   */
  async getCachedProjects(): Promise<Project[]> {
    const cached = await getItem<{ data: Project[]; cachedAt: string }>(
      STORAGE_KEYS.CACHED_PROJECTS
    );
    return cached?.data || [];
  }

  /**
   * Кэширование проверок
   */
  async cacheInspections(inspections: Inspection[]): Promise<void> {
    await setItem(STORAGE_KEYS.CACHED_INSPECTIONS, {
      data: inspections,
      cachedAt: new Date().toISOString(),
    });
  }

  /**
   * Получение кэшированных проверок
   */
  async getCachedInspections(): Promise<Inspection[]> {
    const cached = await getItem<{ data: Inspection[]; cachedAt: string }>(
      STORAGE_KEYS.CACHED_INSPECTIONS
    );
    return cached?.data || [];
  }

  /**
   * Сохранение фото локально для последующей загрузки
   */
  async savePhotoForUpload(
    photoUri: string,
    metadata: {
      inspectionId: number;
      latitude?: number;
      longitude?: number;
      takenAt: string;
    }
  ): Promise<void> {
    const pendingPhotos = (await getItem<any[]>('pending_photos')) || [];

    pendingPhotos.push({
      id: `photo_${Date.now()}`,
      uri: photoUri,
      metadata,
      status: 'pending',
    });

    await setItem('pending_photos', pendingPhotos);
  }

  /**
   * Получение фото для загрузки
   */
  async getPendingPhotos(): Promise<any[]> {
    return (await getItem<any[]>('pending_photos')) || [];
  }

  /**
   * Удаление фото из очереди загрузки
   */
  async removePendingPhoto(photoId: string): Promise<void> {
    const pendingPhotos = await this.getPendingPhotos();
    const filtered = pendingPhotos.filter((photo) => photo.id !== photoId);
    await setItem('pending_photos', filtered);
  }

  /**
   * Проверка доступности данных
   */
  async hasOfflineData(): Promise<boolean> {
    const projects = await this.getCachedProjects();
    const inspections = await this.getCachedInspections();
    return projects.length > 0 || inspections.length > 0;
  }

  /**
   * Очистка кэша
   */
  async clearCache(): Promise<void> {
    await setItem(STORAGE_KEYS.CACHED_PROJECTS, null);
    await setItem(STORAGE_KEYS.CACHED_INSPECTIONS, null);
    await setItem('pending_photos', []);
  }

  /**
   * Получение статистики офлайн-данных
   */
  async getOfflineStats(): Promise<{
    cachedProjects: number;
    cachedInspections: number;
    pendingPhotos: number;
    pendingActions: number;
  }> {
    const projects = await this.getCachedProjects();
    const inspections = await this.getCachedInspections();
    const photos = await this.getPendingPhotos();

    // Получение количества ожидающих действий из очереди
    // const pendingActions = await OfflineQueue.count();

    return {
      cachedProjects: projects.length,
      cachedInspections: inspections.length,
      pendingPhotos: photos.length,
      pendingActions: 0, // pendingActions
    };
  }

  /**
   * Проверка, работает ли приложение в офлайн-режиме
   */
  async isOfflineMode(): Promise<boolean> {
    return !(await isConnected());
  }
}

// Singleton экземпляр
export const offlineService = new OfflineService();
