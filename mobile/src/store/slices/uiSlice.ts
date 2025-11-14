/**
 * Redux Slice для UI состояния
 */
import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { AppSettings } from '../../types';

interface UIState {
  isOnline: boolean;
  syncInProgress: boolean;
  lastSyncTime: string | null;
  settings: AppSettings;
  notification: {
    visible: boolean;
    message: string;
    type: 'success' | 'error' | 'info' | 'warning';
  } | null;
}

const initialState: UIState = {
  isOnline: true,
  syncInProgress: false,
  lastSyncTime: null,
  settings: {
    theme: 'light',
    language: 'ru',
    notifications_enabled: true,
    auto_sync: true,
    photo_quality: 0.8,
    offline_mode: false,
  },
  notification: null,
};

const uiSlice = createSlice({
  name: 'ui',
  initialState,
  reducers: {
    setOnlineStatus: (state, action: PayloadAction<boolean>) => {
      state.isOnline = action.payload;
    },
    setSyncInProgress: (state, action: PayloadAction<boolean>) => {
      state.syncInProgress = action.payload;
    },
    setLastSyncTime: (state, action: PayloadAction<string>) => {
      state.lastSyncTime = action.payload;
    },
    updateSettings: (state, action: PayloadAction<Partial<AppSettings>>) => {
      state.settings = { ...state.settings, ...action.payload };
    },
    showNotification: (
      state,
      action: PayloadAction<{
        message: string;
        type: 'success' | 'error' | 'info' | 'warning';
      }>
    ) => {
      state.notification = {
        visible: true,
        message: action.payload.message,
        type: action.payload.type,
      };
    },
    hideNotification: (state) => {
      if (state.notification) {
        state.notification.visible = false;
      }
    },
    clearNotification: (state) => {
      state.notification = null;
    },
  },
});

export const {
  setOnlineStatus,
  setSyncInProgress,
  setLastSyncTime,
  updateSettings,
  showNotification,
  hideNotification,
  clearNotification,
} = uiSlice.actions;

export default uiSlice.reducer;
