/**
 * Утилиты форматирования
 */

export const formatPhone = (phone: string): string => {
  // Форматирование российского номера: +7 (999) 123-45-67
  const cleaned = phone.replace(/\D/g, '');

  if (cleaned.length === 11 && cleaned[0] === '7') {
    return `+7 (${cleaned.slice(1, 4)}) ${cleaned.slice(4, 7)}-${cleaned.slice(7, 9)}-${cleaned.slice(9, 11)}`;
  }

  return phone;
};

export const formatCurrency = (amount: number, currency: string = '₽'): string => {
  return `${amount.toLocaleString('ru-RU')} ${currency}`;
};

export const formatFileSize = (bytes: number): string => {
  if (bytes === 0) return '0 Bytes';

  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));

  return Math.round((bytes / Math.pow(k, i)) * 100) / 100 + ' ' + sizes[i];
};

export const truncateText = (text: string, maxLength: number): string => {
  if (text.length <= maxLength) return text;
  return text.substring(0, maxLength) + '...';
};

export const formatPercentage = (value: number, decimals: number = 1): string => {
  return `${value.toFixed(decimals)}%`;
};

export const formatCoordinates = (lat: number, lon: number): string => {
  return `${lat.toFixed(6)}, ${lon.toFixed(6)}`;
};
