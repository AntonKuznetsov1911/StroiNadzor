"""
WebSocket endpoints для real-time обновлений
"""
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, Query
from app.websocket import manager, handle_websocket_message
from app.dependencies import get_current_user_ws
from app.models import User
import logging
import json

router = APIRouter()
logger = logging.getLogger(__name__)


@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    token: str = Query(..., description="JWT токен для авторизации"),
    project_id: int = Query(None, description="ID проекта (опционально)")
):
    """
    WebSocket endpoint для real-time обновлений

    Параметры:
    - token: JWT токен для авторизации
    - project_id: ID проекта для подписки (опционально)

    Примеры сообщений от клиента:
    - {"type": "ping"} - проверка соединения
    - {"type": "subscribe_project", "project_id": 1} - подписаться на проект
    - {"type": "unsubscribe_project", "project_id": 1} - отписаться от проекта
    - {"type": "get_stats"} - получить статистику подключений

    Сообщения от сервера:
    - {"type": "connection_established", ...} - соединение установлено
    - {"type": "pong", ...} - ответ на ping
    - {"type": "inspection_created", ...} - создана новая проверка
    - {"type": "inspection_updated", ...} - обновлена проверка
    - {"type": "photo_uploaded", ...} - загружено фото
    - {"type": "defect_detected", ...} - обнаружен дефект
    - {"type": "project_updated", ...} - обновлен проект
    """
    try:
        # Авторизация пользователя по токену
        # (в реальном проекте нужно валидировать JWT токен)
        # Пока используем упрощенный вариант
        user_id = 1  # В реальности: decode JWT token

        # Подключаем WebSocket
        await manager.connect(
            websocket,
            user_id=user_id,
            project_id=project_id,
            metadata={"token": token}
        )

        try:
            # Основной цикл обработки сообщений
            while True:
                # Получаем сообщение от клиента
                data = await websocket.receive_text()

                try:
                    # Парсим JSON
                    message = json.loads(data)

                    # Обрабатываем сообщение
                    await handle_websocket_message(websocket, message)

                except json.JSONDecodeError:
                    # Ошибка парсинга JSON
                    await manager.send_personal_message(
                        websocket,
                        {
                            "type": "error",
                            "message": "Invalid JSON format"
                        }
                    )

        except WebSocketDisconnect:
            # Клиент отключился
            manager.disconnect(websocket)
            logger.info(f"Client disconnected: user_id={user_id}")

    except Exception as e:
        # Ошибка подключения/авторизации
        logger.error(f"WebSocket error: {e}", exc_info=True)
        try:
            await websocket.close(code=1008, reason=str(e))
        except:
            pass


@router.get("/ws/stats")
async def get_websocket_stats():
    """
    Получить статистику WebSocket подключений

    Возвращает:
    - total_connections: Общее количество подключений
    - connected_users: Количество подключенных пользователей
    - users: Список ID подключенных пользователей
    """
    return {
        "total_connections": manager.get_total_connections(),
        "connected_users": len(manager.get_connected_users()),
        "users": manager.get_connected_users()
    }


@router.post("/ws/broadcast")
async def broadcast_message(
    message: dict,
    current_user: User = Depends(get_current_user_ws)
):
    """
    Отправить broadcast сообщение всем подключенным клиентам
    (только для администраторов)

    Параметры:
    - message: Сообщение для отправки
    """
    # Проверка прав (только admin)
    if current_user.role != "admin":
        return {"error": "Access denied"}

    await manager.broadcast(message)

    return {
        "status": "success",
        "message": "Broadcast sent",
        "recipients": manager.get_total_connections()
    }


@router.post("/ws/notify/project/{project_id}")
async def notify_project(
    project_id: int,
    message: dict,
    current_user: User = Depends(get_current_user_ws)
):
    """
    Отправить уведомление всем подключенным к проекту

    Параметры:
    - project_id: ID проекта
    - message: Сообщение для отправки
    """
    await manager.send_to_project(project_id, message)

    return {
        "status": "success",
        "project_id": project_id,
        "recipients": manager.get_project_connections(project_id)
    }
