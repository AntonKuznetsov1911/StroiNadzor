/**
 * Hook для работы с сетью
 */
import { useState, useEffect, useCallback } from 'react';
import {
  getNetworkState,
  subscribeToNetworkChanges,
  NetworkState,
} from '../utils/network';

export function useNetwork() {
  const [networkState, setNetworkState] = useState<NetworkState>({
    isConnected: true,
    isInternetReachable: true,
    type: 'wifi',
  });

  /**
   * Обновление состояния сети
   */
  const refreshNetworkState = useCallback(async () => {
    const state = await getNetworkState();
    setNetworkState(state);
  }, []);

  /**
   * Подписка на изменения сети
   */
  useEffect(() => {
    // Начальная загрузка
    refreshNetworkState();

    // Подписка на изменения
    const unsubscribe = subscribeToNetworkChanges((state) => {
      setNetworkState(state);
    });

    return () => {
      unsubscribe();
    };
  }, [refreshNetworkState]);

  return {
    isConnected: networkState.isConnected,
    isInternetReachable: networkState.isInternetReachable,
    networkType: networkState.type,
    isWifi: networkState.type === 'wifi',
    isCellular: networkState.type === 'cellular',
    isConnectionExpensive:
      networkState.details?.isConnectionExpensive ?? false,
    cellularGeneration: networkState.details?.cellularGeneration,
    refresh: refreshNetworkState,
  };
}
