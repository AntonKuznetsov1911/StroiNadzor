"""
WebSocket handler для real-time обновлений
"""
import json
import logging
from typing import Dict, Set, List
from fastapi import WebSocket, WebSocketDisconnect
from datetime import datetime

logger = logging.getLogger(__name__)


class ConnectionManager:
    """
    Менеджер WebSocket подключений для real-time обновлений
    """

    def __init__(self):
        # Активные подключения: {user_id: Set[WebSocket]}
        self.active_connections: Dict[int, Set[WebSocket]] = {}
        # Подключения по проектам: {project_id: Set[WebSocket]}
        self.project_connections: Dict[int, Set[WebSocket]] = {}
        # Метаданные подключений: {WebSocket: dict}
        self.connection_metadata: Dict[WebSocket, dict] = {}

    async def connect(
        self,
        websocket: WebSocket,
        user_id: int,
        project_id: int = None,
        metadata: dict = None
    ):
        """
        Подключение нового WebSocket клиента

        Args:
            websocket: WebSocket соединение
            user_id: ID пользователя
            project_id: ID проекта (опционально)
            metadata: Дополнительные метаданные
        """
        await websocket.accept()

        # Добавляем в список активных подключений
        if user_id not in self.active_connections:
            self.active_connections[user_id] = set()
        self.active_connections[user_id].add(websocket)

        # Добавляем в список подключений проекта
        if project_id:
            if project_id not in self.project_connections:
                self.project_connections[project_id] = set()
            self.project_connections[project_id].add(websocket)

        # Сохраняем метаданные
        self.connection_metadata[websocket] = {
            "user_id": user_id,
            "project_id": project_id,
            "connected_at": datetime.now(),
            **(metadata or {})
        }

        logger.info(
            f"WebSocket connected: user_id={user_id}, "
            f"project_id={project_id}, total_connections={self.get_total_connections()}"
        )

        # Отправляем приветственное сообщение
        await self.send_personal_message(
            websocket,
            {
                "type": "connection_established",
                "message": "Connected to ТехНадзор real-time updates",
                "timestamp": datetime.now().isoformat()
            }
        )

    def disconnect(self, websocket: WebSocket):
        """
        Отключение WebSocket клиента

        Args:
            websocket: WebSocket соединение
        """
        metadata = self.connection_metadata.get(websocket, {})
        user_id = metadata.get("user_id")
        project_id = metadata.get("project_id")

        # Удаляем из активных подключений
        if user_id and user_id in self.active_connections:
            self.active_connections[user_id].discard(websocket)
            if not self.active_connections[user_id]:
                del self.active_connections[user_id]

        # Удаляем из подключений проекта
        if project_id and project_id in self.project_connections:
            self.project_connections[project_id].discard(websocket)
            if not self.project_connections[project_id]:
                del self.project_connections[project_id]

        # Удаляем метаданные
        if websocket in self.connection_metadata:
            del self.connection_metadata[websocket]

        logger.info(
            f"WebSocket disconnected: user_id={user_id}, "
            f"project_id={project_id}, total_connections={self.get_total_connections()}"
        )

    async def send_personal_message(self, websocket: WebSocket, message: dict):
        """
        Отправка сообщения конкретному WebSocket подключению

        Args:
            websocket: WebSocket соединение
            message: Сообщение (dict)
        """
        try:
            await websocket.send_json(message)
        except Exception as e:
            logger.error(f"Error sending message: {e}")
            self.disconnect(websocket)

    async def send_to_user(self, user_id: int, message: dict):
        """
        Отправка сообщения всем подключениям пользователя

        Args:
            user_id: ID пользователя
            message: Сообщение (dict)
        """
        if user_id in self.active_connections:
            disconnected = []
            for websocket in self.active_connections[user_id]:
                try:
                    await websocket.send_json(message)
                except Exception as e:
                    logger.error(f"Error sending to user {user_id}: {e}")
                    disconnected.append(websocket)

            # Очистка отключенных соединений
            for ws in disconnected:
                self.disconnect(ws)

    async def send_to_project(self, project_id: int, message: dict):
        """
        Отправка сообщения всем подключениям проекта

        Args:
            project_id: ID проекта
            message: Сообщение (dict)
        """
        if project_id in self.project_connections:
            disconnected = []
            for websocket in self.project_connections[project_id]:
                try:
                    await websocket.send_json(message)
                except Exception as e:
                    logger.error(f"Error sending to project {project_id}: {e}")
                    disconnected.append(websocket)

            # Очистка отключенных соединений
            for ws in disconnected:
                self.disconnect(ws)

    async def broadcast(self, message: dict, exclude: WebSocket = None):
        """
        Отправка сообщения всем активным подключениям

        Args:
            message: Сообщение (dict)
            exclude: WebSocket который нужно исключить
        """
        disconnected = []
        for user_connections in self.active_connections.values():
            for websocket in user_connections:
                if websocket != exclude:
                    try:
                        await websocket.send_json(message)
                    except Exception as e:
                        logger.error(f"Error broadcasting: {e}")
                        disconnected.append(websocket)

        # Очистка отключенных соединений
        for ws in disconnected:
            self.disconnect(ws)

    def get_total_connections(self) -> int:
        """Получить общее количество активных подключений"""
        return sum(len(connections) for connections in self.active_connections.values())

    def get_user_connections(self, user_id: int) -> int:
        """Получить количество подключений пользователя"""
        return len(self.active_connections.get(user_id, set()))

    def get_project_connections(self, project_id: int) -> int:
        """Получить количество подключений к проекту"""
        return len(self.project_connections.get(project_id, set()))

    def get_connected_users(self) -> List[int]:
        """Получить список ID подключенных пользователей"""
        return list(self.active_connections.keys())


# Глобальный экземпляр менеджера
manager = ConnectionManager()


async def handle_websocket_message(websocket: WebSocket, data: dict):
    """
    Обработка входящих WebSocket сообщений

    Args:
        websocket: WebSocket соединение
        data: Данные сообщения
    """
    message_type = data.get("type")
    metadata = manager.connection_metadata.get(websocket, {})
    user_id = metadata.get("user_id")

    logger.info(f"WebSocket message received: type={message_type}, user_id={user_id}")

    if message_type == "ping":
        # Ответ на ping
        await manager.send_personal_message(
            websocket,
            {"type": "pong", "timestamp": datetime.now().isoformat()}
        )

    elif message_type == "subscribe_project":
        # Подписка на обновления проекта
        project_id = data.get("project_id")
        if project_id:
            if project_id not in manager.project_connections:
                manager.project_connections[project_id] = set()
            manager.project_connections[project_id].add(websocket)
            metadata["project_id"] = project_id

            await manager.send_personal_message(
                websocket,
                {
                    "type": "subscribed",
                    "project_id": project_id,
                    "message": f"Subscribed to project {project_id}"
                }
            )

    elif message_type == "unsubscribe_project":
        # Отписка от обновлений проекта
        project_id = data.get("project_id")
        if project_id and project_id in manager.project_connections:
            manager.project_connections[project_id].discard(websocket)
            if not manager.project_connections[project_id]:
                del manager.project_connections[project_id]

            await manager.send_personal_message(
                websocket,
                {
                    "type": "unsubscribed",
                    "project_id": project_id,
                    "message": f"Unsubscribed from project {project_id}"
                }
            )

    elif message_type == "get_stats":
        # Получить статистику подключений
        await manager.send_personal_message(
            websocket,
            {
                "type": "stats",
                "total_connections": manager.get_total_connections(),
                "connected_users": len(manager.get_connected_users()),
                "your_connections": manager.get_user_connections(user_id)
            }
        )

    else:
        # Неизвестный тип сообщения
        await manager.send_personal_message(
            websocket,
            {
                "type": "error",
                "message": f"Unknown message type: {message_type}"
            }
        )


# Event handlers для уведомлений о событиях
async def notify_inspection_created(inspection_id: int, project_id: int, data: dict):
    """Уведомление о создании новой проверки"""
    await manager.send_to_project(
        project_id,
        {
            "type": "inspection_created",
            "inspection_id": inspection_id,
            "project_id": project_id,
            "data": data,
            "timestamp": datetime.now().isoformat()
        }
    )


async def notify_inspection_updated(inspection_id: int, project_id: int, data: dict):
    """Уведомление об обновлении проверки"""
    await manager.send_to_project(
        project_id,
        {
            "type": "inspection_updated",
            "inspection_id": inspection_id,
            "project_id": project_id,
            "data": data,
            "timestamp": datetime.now().isoformat()
        }
    )


async def notify_photo_uploaded(photo_id: int, inspection_id: int, project_id: int, data: dict):
    """Уведомление о загрузке фото"""
    await manager.send_to_project(
        project_id,
        {
            "type": "photo_uploaded",
            "photo_id": photo_id,
            "inspection_id": inspection_id,
            "project_id": project_id,
            "data": data,
            "timestamp": datetime.now().isoformat()
        }
    )


async def notify_defect_detected(defect_id: int, photo_id: int, project_id: int, data: dict):
    """Уведомление об обнаружении дефекта"""
    await manager.send_to_project(
        project_id,
        {
            "type": "defect_detected",
            "defect_id": defect_id,
            "photo_id": photo_id,
            "project_id": project_id,
            "data": data,
            "timestamp": datetime.now().isoformat()
        }
    )


async def notify_project_updated(project_id: int, data: dict):
    """Уведомление об обновлении проекта"""
    await manager.send_to_project(
        project_id,
        {
            "type": "project_updated",
            "project_id": project_id,
            "data": data,
            "timestamp": datetime.now().isoformat()
        }
    )
