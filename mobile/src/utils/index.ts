/**
 * Экспорт всех утилит
 */

// Date утилиты
export {
  formatDate,
  formatDateTime,
  formatTime,
  getRelativeTime,
  isToday,
  addDays,
} from './date';

// Formatters
export {
  formatPhone,
  formatCurrency,
  formatFileSize,
  truncateText,
  formatPercentage,
  formatCoordinates,
} from './formatters';

// Validation
export {
  validateEmail,
  validatePhone,
  validatePassword,
  validateRequired,
  validateMinLength,
  validateCoordinates,
} from './validation';

// Permissions
export {
  checkPermission,
  requestPermission,
  requestPermissionWithFallback,
  requestMultiplePermissions,
} from './permissions';
export type { PermissionType, PermissionStatus } from './permissions';

// Camera
export {
  checkCameraPermissions,
  getDeviceMetadata,
  createPhotoMetadata,
  validatePhoto,
  getPhotoSize,
  compressPhoto,
  generatePhotoFileName,
  formatCoordinatesForDisplay,
  calculateDistance,
  isWithinProjectBounds,
} from './camera';
export type {
  PhotoMetadata,
  CapturedPhoto,
  PhotoValidationResult,
} from './camera';

// Geolocation
export {
  getCurrentLocation,
  watchLocation,
  isLocationEnabled,
  requestLocationEnable,
  reverseGeocode,
  geocode,
  isAccuracyAcceptable,
  getDirectionName,
} from './geolocation';
export type { Coordinates, LocationError } from './geolocation';

// File
export {
  getFileInfo,
  fileExists,
  deleteFile,
  copyFile,
  moveFile,
  readFileAsText,
  writeTextToFile,
  getFileExtension,
  getMimeType,
  getTemporaryDirectory,
  getDocumentsDirectory,
  getCacheDirectory,
  formatFileSize as formatFileSizeUtil,
  createDirectory,
  readDirectory,
  clearTemporaryFiles,
} from './file';
export type { FileInfo } from './file';

// Network
export {
  getNetworkState,
  isConnected,
  isWifiConnected,
  isCellularConnected,
  isConnectionExpensive,
  subscribeToNetworkChanges,
  pingServer,
  measureDownloadSpeed,
  getConnectionQuality,
  waitForConnection,
  canDownloadLargeFiles,
  getRecommendedQuality,
  retryWithBackoff,
  getNetworkTypeDescription,
} from './network';
export type { NetworkType, NetworkState } from './network';

// Storage
export {
  setItem,
  getItem,
  removeItem,
  clear,
  getAllKeys,
  multiGet,
  multiSet,
  multiRemove,
  STORAGE_KEYS,
  Cache,
  OfflineQueue,
} from './storage';
