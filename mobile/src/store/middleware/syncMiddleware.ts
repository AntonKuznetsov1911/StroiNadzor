/**
 * Redux Middleware для синхронизации
 */
import { Middleware } from '@reduxjs/toolkit';
import { syncService } from '../../services/sync';
import { isConnected } from '../../utils/network';

/**
 * Middleware для автоматической синхронизации действий
 */
export const syncMiddleware: Middleware = (store) => (next) => async (action) => {
  const result = next(action);

  // Список действий, требующих синхронизации
  const syncableActions = [
    'inspections/create',
    'inspections/update',
    'inspections/uploadPhoto',
    'hiddenWorks/create',
    'hiddenWorks/update',
    'hiddenWorks/signAct',
    'projects/update',
  ];

  // Проверяем, требует ли действие синхронизации
  const needsSync = syncableActions.some((type) =>
    action.type.startsWith(type)
  );

  if (needsSync) {
    const connected = await isConnected();

    if (connected) {
      // Если есть подключение, выполняем синхронизацию
      try {
        await syncService.sync();
      } catch (error) {
        console.error('Sync failed:', error);
      }
    } else {
      // Если нет подключения, добавляем в очередь
      await syncService.queueOfflineAction(action.type, action.payload);
    }
  }

  return result;
};
