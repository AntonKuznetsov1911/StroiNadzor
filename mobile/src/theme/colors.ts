/**
 * Цветовая палитра приложения
 */

export const colors = {
  // Primary
  primary: '#1E3A8A',
  primaryLight: '#3B82F6',
  primaryDark: '#1E40AF',

  // Accent
  accent: '#F97316',
  accentLight: '#FB923C',
  accentDark: '#EA580C',

  // Success
  success: '#10B981',
  successLight: '#34D399',
  successDark: '#059669',

  // Error
  error: '#EF4444',
  errorLight: '#F87171',
  errorDark: '#DC2626',

  // Warning
  warning: '#EAB308',
  warningLight: '#FBBF24',
  warningDark: '#CA8A04',

  // Info
  info: '#3B82F6',
  infoLight: '#60A5FA',
  infoDark: '#2563EB',

  // Neutral
  white: '#FFFFFF',
  black: '#000000',
  gray50: '#F9FAFB',
  gray100: '#F3F4F6',
  gray200: '#E5E7EB',
  gray300: '#D1D5DB',
  gray400: '#9CA3AF',
  gray500: '#6B7280',
  gray600: '#4B5563',
  gray700: '#374151',
  gray800: '#1F2937',
  gray900: '#111827',

  // Backgrounds
  background: '#F9FAFB',
  backgroundDark: '#1F2937',
  surface: '#FFFFFF',
  surfaceDark: '#374151',

  // Text
  textPrimary: '#1F2937',
  textSecondary: '#6B7280',
  textTertiary: '#9CA3AF',
  textInverse: '#FFFFFF',

  // Borders
  border: '#E5E7EB',
  borderDark: '#D1D5DB',
};

export type ColorKey = keyof typeof colors;
