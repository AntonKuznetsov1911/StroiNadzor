/**
 * Hook для работы с геолокацией
 */
import { useState, useEffect, useCallback } from 'react';
import {
  getCurrentLocation,
  watchLocation,
  Coordinates,
  LocationError,
} from '../utils/geolocation';

export interface UseLocationOptions {
  watch?: boolean;
  enableHighAccuracy?: boolean;
  timeout?: number;
  maximumAge?: number;
}

export function useLocation(options: UseLocationOptions = {}) {
  const [location, setLocation] = useState<Coordinates | null>(null);
  const [error, setError] = useState<LocationError | null>(null);
  const [loading, setLoading] = useState(true);

  /**
   * Получение текущей геолокации
   */
  const fetchLocation = useCallback(async () => {
    setLoading(true);
    setError(null);

    try {
      const coords = await getCurrentLocation();
      setLocation(coords);
    } catch (err) {
      setError(err as LocationError);
    } finally {
      setLoading(false);
    }
  }, []);

  /**
   * Начальная загрузка
   */
  useEffect(() => {
    fetchLocation();
  }, [fetchLocation]);

  /**
   * Наблюдение за изменением локации
   */
  useEffect(() => {
    if (!options.watch) return;

    const unwatch = watchLocation(
      (coords) => {
        setLocation(coords);
        setLoading(false);
      },
      (err) => {
        setError(err);
        setLoading(false);
      }
    );

    return () => {
      unwatch();
    };
  }, [options.watch]);

  /**
   * Обновление локации вручную
   */
  const refresh = useCallback(() => {
    fetchLocation();
  }, [fetchLocation]);

  return {
    location,
    error,
    loading,
    refresh,
  };
}
