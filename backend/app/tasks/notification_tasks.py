"""
Задачи для уведомлений
"""
from celery import Task
from app.celery_app import celery_app
from app.database import SessionLocal
from app.models.hidden_works import HiddenWork, HiddenWorkStatus
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class NotificationTask(Task):
    """Базовый класс для задач уведомлений"""

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        logger.error(f"Notification Task {task_id} failed: {exc}")
        super().on_failure(exc, task_id, args, kwargs, einfo)


@celery_app.task(base=NotificationTask, name="app.tasks.notification_tasks.send_email_notification")
def send_email_notification(user_email: str, subject: str, message: str):
    """
    Отправка email уведомления

    TODO: Интеграция с SMTP или Email сервисом
    """
    logger.info(f"Sending email to {user_email}: {subject}")

    # ЗАГЛУШКА: В продакшене здесь будет отправка email
    # import smtplib
    # from email.mime.text import MIMEText

    return {
        "email": user_email,
        "subject": subject,
        "status": "sent"
    }


@celery_app.task(base=NotificationTask, name="app.tasks.notification_tasks.send_push_notification")
def send_push_notification(user_id: int, title: str, body: str):
    """
    Отправка push уведомления

    TODO: Интеграция с Firebase Cloud Messaging или другим сервисом
    """
    logger.info(f"Sending push notification to user {user_id}: {title}")

    # ЗАГЛУШКА: В продакшене здесь будет отправка push
    # from firebase_admin import messaging

    return {
        "user_id": user_id,
        "title": title,
        "status": "sent"
    }


@celery_app.task(name="app.tasks.notification_tasks.check_hidden_works_deadlines")
def check_hidden_works_deadlines():
    """
    Периодическая проверка дедлайнов скрытых работ
    Отправляет уведомления о приближающихся дедлайнах
    """
    db = SessionLocal()

    try:
        # Ищем работы с приближающимися дедлайнами (менее 24 часов)
        tomorrow = datetime.utcnow() + timedelta(days=1)

        pending_works = db.query(HiddenWork).filter(
            HiddenWork.status == HiddenWorkStatus.PENDING,
            HiddenWork.closing_deadline <= tomorrow,
            HiddenWork.closing_deadline > datetime.utcnow(),
            HiddenWork.notification_sent == False
        ).all()

        logger.info(f"Found {len(pending_works)} works with approaching deadlines")

        for work in pending_works:
            # Отправляем уведомление
            send_push_notification.delay(
                user_id=work.project.created_by,
                title="Приближается дедлайн",
                body=f"Скрытые работы '{work.title}' должны быть проверены до {work.closing_deadline.strftime('%d.%m.%Y %H:%M')}"
            )

            # Помечаем что уведомление отправлено
            work.notification_sent = True
            work.notification_sent_at = datetime.utcnow()

        db.commit()

        return {
            "works_notified": len(pending_works),
            "status": "success"
        }

    except Exception as e:
        logger.error(f"Error checking deadlines: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()
