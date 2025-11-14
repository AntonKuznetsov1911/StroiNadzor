"""
ML задачи для распознавания дефектов
"""
from celery import Task
from app.celery_app import celery_app
from app.database import SessionLocal
from app.models.inspection import InspectionPhoto, DefectDetection
import logging

logger = logging.getLogger(__name__)


class MLTask(Task):
    """Базовый класс для ML задач"""

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        logger.error(f"ML Task {task_id} failed: {exc}")
        super().on_failure(exc, task_id, args, kwargs, einfo)


@celery_app.task(base=MLTask, name="app.tasks.ml_tasks.analyze_photo")
def analyze_photo(photo_id: int):
    """
    Анализ фотографии с помощью ML модели для обнаружения дефектов

    TODO: Интеграция с реальной ML моделью (YOLOv8)
    """
    db = SessionLocal()

    try:
        photo = db.query(InspectionPhoto).filter(InspectionPhoto.id == photo_id).first()

        if not photo:
            logger.error(f"Photo {photo_id} not found")
            return

        logger.info(f"Analyzing photo {photo_id}: {photo.file_url}")

        # ЗАГЛУШКА: В продакшене здесь будет вызов ML модели
        # Пример:
        # from app.services.ml_service import detect_defects
        # detections = detect_defects(photo.file_url)

        # Симуляция обнаружения дефекта
        demo_detections = [
            {
                "defect_type": "crack",
                "severity": "major",
                "description": "Обнаружена трещина в бетоне",
                "confidence_score": 0.92,
                "bbox_x": 0.3,
                "bbox_y": 0.4,
                "bbox_width": 0.2,
                "bbox_height": 0.15,
            }
        ]

        # Сохранение обнаруженных дефектов
        for detection_data in demo_detections:
            defect = DefectDetection(
                photo_id=photo_id,
                detected_by_ai=True,
                **detection_data
            )
            db.add(defect)

        # Обновление статуса фото
        photo.ai_analyzed = True
        photo.ai_analysis_result = f"Found {len(demo_detections)} defects"

        db.commit()

        logger.info(f"Photo {photo_id} analyzed successfully. Found {len(demo_detections)} defects")

        return {
            "photo_id": photo_id,
            "defects_found": len(demo_detections),
            "status": "success"
        }

    except Exception as e:
        logger.error(f"Error analyzing photo {photo_id}: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()


@celery_app.task(name="app.tasks.ml_tasks.batch_analyze_inspection")
def batch_analyze_inspection(inspection_id: int):
    """
    Пакетный анализ всех фотографий проверки
    """
    db = SessionLocal()

    try:
        photos = db.query(InspectionPhoto).filter(
            InspectionPhoto.inspection_id == inspection_id,
            InspectionPhoto.ai_analyzed == False
        ).all()

        logger.info(f"Starting batch analysis for inspection {inspection_id}. {len(photos)} photos to analyze")

        results = []
        for photo in photos:
            result = analyze_photo.delay(photo.id)
            results.append(result.id)

        return {
            "inspection_id": inspection_id,
            "photos_count": len(photos),
            "task_ids": results
        }

    except Exception as e:
        logger.error(f"Error in batch analysis: {str(e)}")
        raise
    finally:
        db.close()
