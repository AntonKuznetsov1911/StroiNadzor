/**
 * API конфигурация
 */

// Замените на ваш API URL
export const API_BASE_URL = __DEV__
  ? 'http://localhost:8000/api/v1'
  : 'https://api.tehnadzor.ru/api/v1';

export const API_ENDPOINTS = {
  // Auth
  LOGIN: '/auth/login',
  REGISTER: '/auth/register',
  ME: '/auth/me',

  // Projects
  PROJECTS: '/projects',
  PROJECT_DETAIL: (id: number) => `/projects/${id}`,

  // Inspections
  INSPECTIONS: '/inspections',
  INSPECTION_DETAIL: (id: number) => `/inspections/${id}`,
  INSPECTION_PHOTOS: (inspectionId: number) => `/inspections/${inspectionId}/photos`,
  INSPECTION_ANALYZE: (inspectionId: number) => `/inspections/${inspectionId}/analyze`,

  // Hidden Works
  HIDDEN_WORKS: '/hidden-works',
  HIDDEN_WORK_DETAIL: (id: number) => `/hidden-works/${id}`,
  HIDDEN_WORK_ACTS: (workId: number) => `/hidden-works/${workId}/acts`,

  // Regulations
  REGULATIONS: '/regulations',
  REGULATION_DETAIL: (id: number) => `/regulations/${id}`,
  AI_CONSULT: '/regulations/ai-consult',
  SEMANTIC_SEARCH: '/regulations/search-semantic',
};

export const API_CONFIG = {
  TIMEOUT: 30000, // 30 seconds
  RETRY_ATTEMPTS: 3,
};
