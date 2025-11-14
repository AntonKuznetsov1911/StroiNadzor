/**
 * Инициализация WatermelonDB
 */
import { Database } from '@nozbe/watermelondb';
import SQLiteAdapter from '@nozbe/watermelondb/adapters/sqlite';

import { schema } from './schema';
import * as models from './models';

// Конфигурация SQLite адаптера
const adapter = new SQLiteAdapter({
  schema,
  // Опционально: миграции для обновления схемы
  // migrations,
  jsi: true, // Используем JSI для лучшей производительности
  onSetUpError: (error) => {
    console.error('Database setup error:', error);
  },
});

// Создание экземпляра базы данных
export const database = new Database({
  adapter,
  modelClasses: [
    models.Project,
    models.Inspection,
    models.InspectionPhoto,
    models.DefectDetection,
    models.HiddenWork,
    models.Document,
    models.SyncQueue,
  ],
});

// Экспорт для использования в приложении
export { models };
export * from './sync';
