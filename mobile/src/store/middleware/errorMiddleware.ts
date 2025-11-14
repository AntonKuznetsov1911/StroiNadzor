/**
 * Redux Middleware для обработки ошибок
 */
import { Middleware } from '@reduxjs/toolkit';
import { Alert } from 'react-native';

/**
 * Middleware для обработки ошибок в действиях
 */
export const errorMiddleware: Middleware = () => (next) => (action) => {
  // Проверяем, является ли действие отклоненным промисом
  if (action.type.endsWith('/rejected')) {
    const errorMessage = action.error?.message || 'Произошла ошибка';

    // Показываем алерт с ошибкой
    if (__DEV__) {
      console.error('Redux Error:', errorMessage, action);
    }

    // Показываем пользователю только в production или для критических ошибок
    if (!__DEV__ || action.error?.critical) {
      Alert.alert('Ошибка', errorMessage);
    }
  }

  return next(action);
};
