"""
Задачи для генерации документов
"""
from celery import Task
from app.celery_app import celery_app
from app.database import SessionLocal
from app.models.hidden_works import HiddenWorkAct
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class DocumentTask(Task):
    """Базовый класс для задач генерации документов"""

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        logger.error(f"Document Task {task_id} failed: {exc}")
        super().on_failure(exc, task_id, args, kwargs, einfo)


@celery_app.task(base=DocumentTask, name="app.tasks.document_tasks.generate_hidden_work_act")
def generate_hidden_work_act(act_id: int):
    """
    Генерация PDF акта освидетельствования скрытых работ

    TODO: Интеграция с ReportLab для генерации PDF
    """
    db = SessionLocal()

    try:
        act = db.query(HiddenWorkAct).filter(HiddenWorkAct.id == act_id).first()

        if not act:
            logger.error(f"Act {act_id} not found")
            return

        logger.info(f"Generating PDF for act {act.act_number}")

        # ЗАГЛУШКА: В продакшене здесь будет генерация PDF
        # from app.services.document_service import generate_act_pdf
        # pdf_path = generate_act_pdf(act)

        # Симуляция генерации PDF
        pdf_filename = f"act_{act.act_number}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        pdf_url = f"/uploads/acts/{pdf_filename}"

        # Обновление акта
        act.document_url = pdf_url
        db.commit()

        logger.info(f"PDF generated successfully for act {act.act_number}: {pdf_url}")

        return {
            "act_id": act_id,
            "act_number": act.act_number,
            "document_url": pdf_url,
            "status": "success"
        }

    except Exception as e:
        logger.error(f"Error generating PDF for act {act_id}: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()


@celery_app.task(base=DocumentTask, name="app.tasks.document_tasks.generate_inspection_report")
def generate_inspection_report(inspection_id: int):
    """
    Генерация отчета по проверке
    """
    logger.info(f"Generating inspection report for inspection {inspection_id}")

    # TODO: Реализация генерации отчета

    return {
        "inspection_id": inspection_id,
        "status": "success"
    }
