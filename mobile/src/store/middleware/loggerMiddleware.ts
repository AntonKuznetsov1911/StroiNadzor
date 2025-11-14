/**
 * Redux Middleware для логирования
 */
import { Middleware } from '@reduxjs/toolkit';

/**
 * Middleware для логирования действий Redux
 */
export const loggerMiddleware: Middleware = (store) => (next) => (action) => {
  if (__DEV__) {
    console.group(`Action: ${action.type}`);
    console.log('Previous State:', store.getState());
    console.log('Action:', action);

    const result = next(action);

    console.log('Next State:', store.getState());
    console.groupEnd();

    return result;
  }

  return next(action);
};
