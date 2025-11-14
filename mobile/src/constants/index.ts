/**
 * Константы приложения
 */

// API
export const API_BASE_URL = __DEV__
  ? 'http://localhost:8000/api/v1'
  : 'https://api.tehnadzor.ru/api/v1';

export const API_TIMEOUT = 30000; // 30 секунд

// Размеры
export const SCREEN_PADDING = 16;
export const CARD_BORDER_RADIUS = 12;
export const INPUT_HEIGHT = 48;

// Лимиты
export const MAX_PHOTO_SIZE_MB = 10;
export const MAX_PHOTOS_PER_INSPECTION = 50;
export const PHOTO_QUALITY = 0.8;
export const PHOTO_MAX_WIDTH = 1920;
export const PHOTO_MAX_HEIGHT = 1080;

// Геолокация
export const LOCATION_ACCURACY_THRESHOLD = 50; // метров
export const PROJECT_RADIUS_METERS = 1000; // Радиус проекта для проверки координат

// Кэш
export const CACHE_TTL_SHORT = 5 * 60 * 1000; // 5 минут
export const CACHE_TTL_MEDIUM = 30 * 60 * 1000; // 30 минут
export const CACHE_TTL_LONG = 24 * 60 * 60 * 1000; // 24 часа

// Синхронизация
export const SYNC_INTERVAL = 15 * 60 * 1000; // 15 минут
export const OFFLINE_QUEUE_MAX_SIZE = 100;

// Пагинация
export const PAGE_SIZE = 20;
export const INITIAL_PAGE = 1;

// Роли пользователей
export const USER_ROLES = {
  ADMIN: 'admin',
  ENGINEER: 'engineer',
  SUPERVISOR: 'supervisor',
  CONTRACTOR: 'contractor',
  VIEWER: 'viewer',
} as const;

// Статусы проектов
export const PROJECT_STATUSES = {
  PLANNING: 'planning',
  IN_PROGRESS: 'in_progress',
  ON_HOLD: 'on_hold',
  COMPLETED: 'completed',
  ARCHIVED: 'archived',
} as const;

// Типы проектов
export const PROJECT_TYPES = {
  RESIDENTIAL: 'residential',
  COMMERCIAL: 'commercial',
  INDUSTRIAL: 'industrial',
  INFRASTRUCTURE: 'infrastructure',
  RENOVATION: 'renovation',
} as const;

// Результаты проверок
export const INSPECTION_RESULTS = {
  PASSED: 'passed',
  FAILED: 'failed',
  WITH_REMARKS: 'with_remarks',
  PENDING: 'pending',
} as const;

// Типы дефектов
export const DEFECT_TYPES = {
  CRACK: 'crack',
  DEVIATION: 'deviation',
  REINFORCEMENT: 'reinforcement',
  WELDING: 'welding',
  WATERPROOFING: 'waterproofing',
  CONCRETE_QUALITY: 'concrete_quality',
  OTHER: 'other',
} as const;

// Степени серьезности дефектов
export const DEFECT_SEVERITIES = {
  CRITICAL: 'critical',
  MAJOR: 'major',
  MINOR: 'minor',
  COSMETIC: 'cosmetic',
} as const;

// Статусы скрытых работ
export const HIDDEN_WORK_STATUSES = {
  PENDING: 'pending',
  APPROVED: 'approved',
  REJECTED: 'rejected',
  REVISION_REQUIRED: 'revision_required',
} as const;

// Типы документов
export const DOCUMENT_TYPES = {
  ACT: 'act',
  REPORT: 'report',
  PRESCRIPTION: 'prescription',
  PROTOCOL: 'protocol',
  CERTIFICATE: 'certificate',
  DRAWING: 'drawing',
  OTHER: 'other',
} as const;

// Форматы экспорта
export const EXPORT_FORMATS = {
  PDF: 'pdf',
  WORD: 'word',
  EXCEL: 'excel',
} as const;

// Регулярные выражения
export const REGEX = {
  EMAIL: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
  PHONE: /^(\+7|8)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$/,
  PASSWORD: /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d@$!%*?&]{8,}$/,
} as const;

// Локализация
export const LOCALE = 'ru-RU';
export const CURRENCY = 'RUB';
export const DATE_FORMAT = 'DD.MM.YYYY';
export const TIME_FORMAT = 'HH:mm';
export const DATETIME_FORMAT = 'DD.MM.YYYY HH:mm';

// Анимация
export const ANIMATION_DURATION = 300;
export const ANIMATION_EASING = 'ease-in-out';

// Уведомления
export const NOTIFICATION_DURATION = 3000;

// Дебаунс
export const DEBOUNCE_DELAY = 500;
export const SEARCH_DEBOUNCE_DELAY = 300;

// Пути навигации
export const ROUTES = {
  // Auth
  LOGIN: 'Login',
  REGISTER: 'Register',
  FORGOT_PASSWORD: 'ForgotPassword',

  // Main
  HOME: 'Home',
  PROJECTS: 'Projects',
  INSPECTIONS: 'Inspections',
  AI_CONSULTANT: 'AIConsultant',
  PROFILE: 'Profile',

  // Details
  PROJECT_DETAIL: 'ProjectDetail',
  INSPECTION_DETAIL: 'InspectionDetail',
  HIDDEN_WORKS: 'HiddenWorks',
  HIDDEN_WORK_DETAIL: 'HiddenWorkDetail',

  // Camera
  CAMERA: 'Camera',
  PHOTO_PREVIEW: 'PhotoPreview',

  // Settings
  SETTINGS: 'Settings',
  NOTIFICATIONS: 'Notifications',
} as const;

// Иконки
export const ICONS = {
  HOME: 'home',
  PROJECTS: 'folder',
  INSPECTIONS: 'clipboard-list',
  AI: 'robot',
  PROFILE: 'user',
  CAMERA: 'camera',
  LOCATION: 'map-marker',
  CALENDAR: 'calendar',
  DOCUMENT: 'file-text',
  SETTINGS: 'settings',
  LOGOUT: 'log-out',
} as const;

// Ошибки
export const ERROR_MESSAGES = {
  NETWORK_ERROR: 'Ошибка сети. Проверьте подключение к интернету.',
  UNAUTHORIZED: 'Необходима авторизация.',
  FORBIDDEN: 'Доступ запрещен.',
  NOT_FOUND: 'Ресурс не найден.',
  SERVER_ERROR: 'Ошибка сервера. Попробуйте позже.',
  VALIDATION_ERROR: 'Ошибка валидации данных.',
  UNKNOWN_ERROR: 'Произошла неизвестная ошибка.',
  LOCATION_PERMISSION_DENIED: 'Отказано в доступе к геолокации.',
  CAMERA_PERMISSION_DENIED: 'Отказано в доступе к камере.',
  GPS_DISABLED: 'GPS отключен. Включите геолокацию.',
  LOCATION_ACCURACY_LOW: 'Низкая точность определения местоположения.',
} as const;

// Успешные сообщения
export const SUCCESS_MESSAGES = {
  LOGIN_SUCCESS: 'Вход выполнен успешно',
  REGISTER_SUCCESS: 'Регистрация выполнена успешно',
  PHOTO_UPLOADED: 'Фото загружено успешно',
  INSPECTION_CREATED: 'Проверка создана успешно',
  ACT_SIGNED: 'Акт подписан успешно',
  SYNC_COMPLETE: 'Синхронизация завершена',
  DATA_SAVED: 'Данные сохранены',
} as const;
