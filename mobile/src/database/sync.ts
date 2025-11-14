/**
 * WatermelonDB синхронизация с сервером
 */
import { synchronize, SyncDatabaseChangeSet } from '@nozbe/watermelondb/sync';
import { database } from './index';
import { apiService } from '../services/apiService';

interface SyncResult {
  success: boolean;
  timestamp?: number;
  error?: string;
}

/**
 * Синхронизация базы данных с сервером
 */
export async function syncDatabase(): Promise<SyncResult> {
  try {
    await synchronize({
      database,
      pullChanges: async ({ lastPulledAt, schemaVersion, migration }) => {
        // Получение изменений с сервера
        const response = await apiService.get('/api/v1/sync/pull', {
          params: {
            last_pulled_at: lastPulledAt || 0,
            schema_version: schemaVersion,
            migration: migration ? JSON.stringify(migration) : null,
          },
        });

        const { changes, timestamp } = response.data;

        return {
          changes: transformServerChanges(changes),
          timestamp,
        };
      },
      pushChanges: async ({ changes, lastPulledAt }) => {
        // Отправка локальных изменений на сервер
        const transformedChanges = transformLocalChanges(changes);

        await apiService.post('/api/v1/sync/push', {
          changes: transformedChanges,
          last_pulled_at: lastPulledAt,
        });
      },
      // Настройки синхронизации
      sendCreatedAsUpdated: true, // Отправлять created как updated для упрощения
      log: __DEV__ ? console.log : undefined,
      conflictResolver: (tableSchema, local, remote) => {
        // Стратегия разрешения конфликтов: сервер всегда выигрывает
        return remote;
      },
    });

    return {
      success: true,
      timestamp: Date.now(),
    };
  } catch (error: any) {
    console.error('Sync error:', error);
    return {
      success: false,
      error: error.message,
    };
  }
}

/**
 * Преобразование изменений с сервера в формат WatermelonDB
 */
function transformServerChanges(serverChanges: any): SyncDatabaseChangeSet {
  const changes: SyncDatabaseChangeSet = {};

  for (const [tableName, tableChanges] of Object.entries(serverChanges)) {
    const { created = [], updated = [], deleted = [] } = tableChanges as any;

    changes[tableName] = {
      created: created.map(transformServerRecord),
      updated: updated.map(transformServerRecord),
      deleted: deleted,
    };
  }

  return changes;
}

/**
 * Преобразование одной записи с сервера
 */
function transformServerRecord(record: any) {
  return {
    id: record.id.toString(),
    server_id: record.id,
    ...transformFieldNames(record),
    synced_at: Date.now(),
    is_dirty: false,
  };
}

/**
 * Преобразование имен полей из snake_case (сервер) в camelCase (клиент)
 */
function transformFieldNames(record: any) {
  const transformed: any = {};

  for (const [key, value] of Object.entries(record)) {
    // Пропускаем служебные поля
    if (key === 'id' || key === 'created_at' || key === 'updated_at') {
      continue;
    }

    // Преобразуем даты в timestamp
    if (key.includes('_date') || key.includes('_at')) {
      transformed[key] = value ? new Date(value as string).getTime() : null;
    } else {
      transformed[key] = value;
    }
  }

  return transformed;
}

/**
 * Преобразование локальных изменений для отправки на сервер
 */
function transformLocalChanges(localChanges: SyncDatabaseChangeSet) {
  const transformed: any = {};

  for (const [tableName, tableChanges] of Object.entries(localChanges)) {
    transformed[tableName] = {
      created: tableChanges.created.map(transformLocalRecord),
      updated: tableChanges.updated.map(transformLocalRecord),
      deleted: tableChanges.deleted,
    };
  }

  return transformed;
}

/**
 * Преобразование одной локальной записи для сервера
 */
function transformLocalRecord(record: any) {
  const transformed: any = {
    ...record,
  };

  // Удаляем локальные поля
  delete transformed.id;
  delete transformed.synced_at;
  delete transformed.is_dirty;
  delete transformed.local_uri;

  // Преобразуем timestamp обратно в ISO строки
  for (const [key, value] of Object.entries(transformed)) {
    if (typeof value === 'number' && (key.includes('_date') || key.includes('_at'))) {
      transformed[key] = new Date(value).toISOString();
    }
  }

  return transformed;
}

/**
 * Пометить запись как требующую синхронизации
 */
export async function markAsDirty(model: any) {
  await model.update((record: any) => {
    record.is_dirty = true;
  });
}

/**
 * Очистить локальную базу данных (для отладки)
 */
export async function resetDatabase() {
  if (__DEV__) {
    await database.write(async () => {
      await database.unsafeResetDatabase();
    });
    console.log('Database reset complete');
  }
}

/**
 * Получить статистику синхронизации
 */
export async function getSyncStats() {
  const collections = database.collections;
  const stats: any = {};

  for (const [name, collection] of Object.entries(collections)) {
    const total = await collection.query().fetchCount();
    const dirty = await collection
      .query()
      // @ts-ignore
      .where('is_dirty', true)
      .fetchCount();

    stats[name] = { total, dirty, synced: total - dirty };
  }

  return stats;
}
