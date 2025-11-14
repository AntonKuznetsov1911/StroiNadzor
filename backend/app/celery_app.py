"""
Celery приложение для фоновых задач
"""
from celery import Celery
from app.config import settings

celery_app = Celery(
    "tehnadzor",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=["app.tasks.ml_tasks", "app.tasks.document_tasks", "app.tasks.notification_tasks"]
)

# Конфигурация Celery
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 минут
    task_soft_time_limit=25 * 60,  # 25 минут
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=1000,
)

# Периодические задачи
celery_app.conf.beat_schedule = {
    "check-hidden-works-deadlines": {
        "task": "app.tasks.notification_tasks.check_hidden_works_deadlines",
        "schedule": 3600.0,  # Каждый час
    },
}
