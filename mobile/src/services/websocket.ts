/**
 * Сервис WebSocket для real-time обновлений
 */
import { API_BASE_URL } from '../constants';

export type WebSocketEventType =
  | 'inspection_created'
  | 'inspection_updated'
  | 'defect_detected'
  | 'hidden_work_approved'
  | 'act_signed'
  | 'sync_required';

export interface WebSocketMessage {
  type: WebSocketEventType;
  data: any;
  timestamp: string;
}

type EventHandler = (data: any) => void;

class WebSocketService {
  private ws: WebSocket | null = null;
  private reconnectInterval: NodeJS.Timeout | null = null;
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 5;
  private eventHandlers: Map<WebSocketEventType, EventHandler[]> = new Map();

  /**
   * Подключение к WebSocket серверу
   */
  connect(token: string): void {
    const wsUrl = API_BASE_URL.replace('http', 'ws').replace('/api/v1', '/ws');

    try {
      this.ws = new WebSocket(`${wsUrl}?token=${token}`);

      this.ws.onopen = this.handleOpen.bind(this);
      this.ws.onmessage = this.handleMessage.bind(this);
      this.ws.onerror = this.handleError.bind(this);
      this.ws.onclose = this.handleClose.bind(this);
    } catch (error) {
      console.error('WebSocket connection error:', error);
    }
  }

  /**
   * Отключение от WebSocket
   */
  disconnect(): void {
    if (this.reconnectInterval) {
      clearInterval(this.reconnectInterval);
      this.reconnectInterval = null;
    }

    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }

    this.reconnectAttempts = 0;
  }

  /**
   * Отправка сообщения
   */
  send(type: string, data: any): void {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      const message = {
        type,
        data,
        timestamp: new Date().toISOString(),
      };
      this.ws.send(JSON.stringify(message));
    } else {
      console.warn('WebSocket is not connected');
    }
  }

  /**
   * Подписка на событие
   */
  on(eventType: WebSocketEventType, handler: EventHandler): () => void {
    if (!this.eventHandlers.has(eventType)) {
      this.eventHandlers.set(eventType, []);
    }

    this.eventHandlers.get(eventType)!.push(handler);

    // Возвращаем функцию для отписки
    return () => {
      const handlers = this.eventHandlers.get(eventType);
      if (handlers) {
        const index = handlers.indexOf(handler);
        if (index > -1) {
          handlers.splice(index, 1);
        }
      }
    };
  }

  /**
   * Обработка открытия соединения
   */
  private handleOpen(): void {
    console.log('WebSocket connected');
    this.reconnectAttempts = 0;

    if (this.reconnectInterval) {
      clearInterval(this.reconnectInterval);
      this.reconnectInterval = null;
    }
  }

  /**
   * Обработка входящих сообщений
   */
  private handleMessage(event: MessageEvent): void {
    try {
      const message: WebSocketMessage = JSON.parse(event.data);
      console.log('WebSocket message received:', message);

      // Вызываем обработчики для данного типа события
      const handlers = this.eventHandlers.get(message.type);
      if (handlers) {
        handlers.forEach((handler) => handler(message.data));
      }
    } catch (error) {
      console.error('Error parsing WebSocket message:', error);
    }
  }

  /**
   * Обработка ошибок
   */
  private handleError(error: Event): void {
    console.error('WebSocket error:', error);
  }

  /**
   * Обработка закрытия соединения
   */
  private handleClose(): void {
    console.log('WebSocket disconnected');

    // Попытка переподключения
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      this.reconnectAttempts++;
      const delay = Math.min(1000 * Math.pow(2, this.reconnectAttempts), 30000);

      console.log(
        `Attempting to reconnect in ${delay}ms (attempt ${this.reconnectAttempts}/${this.maxReconnectAttempts})`
      );

      this.reconnectInterval = setTimeout(() => {
        // Попытка переподключения с сохраненным токеном
        // this.connect(token);
      }, delay);
    } else {
      console.error('Max reconnection attempts reached');
    }
  }

  /**
   * Проверка статуса подключения
   */
  isConnected(): boolean {
    return this.ws !== null && this.ws.readyState === WebSocket.OPEN;
  }

  /**
   * Получение состояния подключения
   */
  getReadyState(): number | null {
    return this.ws?.readyState ?? null;
  }
}

// Singleton экземпляр
export const webSocketService = new WebSocketService();
