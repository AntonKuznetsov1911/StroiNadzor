"""
API Endpoints для генерации документов

Endpoints:
- POST /documents/act - Генерация акта освидетельствования
- POST /documents/report - Генерация отчета по проверке
- POST /documents/prescription - Генерация предписания
- POST /documents/watermark - Добавление водяного знака на фото
"""

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import io

from app.api.deps import get_db, get_current_user
from app.models import User, Inspection, Project, Photo
from app.services.document_service import document_service
from pydantic import BaseModel

router = APIRouter()


# Schemas
class DefectInfo(BaseModel):
    """Информация о дефекте"""
    name: str
    confidence: float
    regulation: Optional[str] = None
    description: Optional[str] = None


class ActGenerateRequest(BaseModel):
    """Запрос на генерацию акта"""
    inspection_id: int
    include_photos: bool = True


class ActManualRequest(BaseModel):
    """Ручной запрос на генерацию акта"""
    act_number: str
    project_name: str
    project_address: Optional[str] = None
    customer: Optional[str] = None
    contractor: Optional[str] = None
    work_type: str = "Скрытые работы"
    inspector_name: str
    gps_lat: Optional[float] = None
    gps_lon: Optional[float] = None
    gps_accuracy: Optional[float] = None
    description: str
    defects: List[DefectInfo] = []


class WatermarkRequest(BaseModel):
    """Запрос на добавление водяного знака"""
    gps_lat: Optional[float] = None
    gps_lon: Optional[float] = None
    project_name: Optional[str] = None


@router.post("/act/generate", summary="Генерация акта освидетельствования")
async def generate_inspection_act(
    request: ActGenerateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Генерация PDF акта освидетельствования на основе проверки

    - **inspection_id**: ID проверки
    - **include_photos**: Включить фотографии в акт
    """

    # Получаем проверку
    inspection = db.query(Inspection).filter(Inspection.id == request.inspection_id).first()
    if not inspection:
        raise HTTPException(status_code=404, detail="Проверка не найдена")

    # Получаем проект
    project = db.query(Project).filter(Project.id == inspection.project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Проект не найден")

    # Получаем фотографии
    photos = []
    if request.include_photos:
        photos = (
            db.query(Photo)
            .filter(Photo.inspection_id == inspection.id)
            .limit(8)
            .all()
        )

    # Получаем дефекты
    defects = []
    if inspection.ai_analysis:
        # Парсим AI анализ (предполагается JSON)
        import json
        try:
            ai_data = json.loads(inspection.ai_analysis)
            defects = ai_data.get("defects", [])
        except:
            pass

    # Подготавливаем данные для акта
    act_data = {
        "act_number": f"{inspection.id}/{datetime.now().year}",
        "date": inspection.created_at.strftime("%d.%m.%Y"),
        "project_name": project.name,
        "project_address": project.address,
        "customer": project.customer,
        "contractor": project.contractor,
        "work_type": inspection.work_type or "Скрытые работы",
        "inspector_name": current_user.full_name,
        "gps_lat": inspection.gps_latitude,
        "gps_lon": inspection.gps_longitude,
        "gps_accuracy": inspection.gps_accuracy,
        "description": inspection.description or "Проведено освидетельствование скрытых работ.",
        "defects": defects,
        "photos": [
            {
                "path": photo.file_path,
                "gps_lat": photo.gps_latitude,
                "gps_lon": photo.gps_longitude,
                "timestamp": photo.timestamp,
            }
            for photo in photos
        ],
    }

    # Генерируем PDF
    pdf_bytes = document_service.generate_act_pdf(act_data)

    # Возвращаем PDF
    return StreamingResponse(
        io.BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=act_{inspection.id}_{datetime.now().strftime('%Y%m%d')}.pdf"
        },
    )


@router.post("/act/manual", summary="Ручная генерация акта")
async def generate_manual_act(
    request: ActManualRequest,
    current_user: User = Depends(get_current_user),
):
    """
    Ручная генерация акта освидетельствования

    Позволяет создать акт без привязки к существующей проверке в БД
    """

    act_data = {
        "act_number": request.act_number,
        "date": datetime.now().strftime("%d.%m.%Y"),
        "project_name": request.project_name,
        "project_address": request.project_address,
        "customer": request.customer,
        "contractor": request.contractor,
        "work_type": request.work_type,
        "inspector_name": request.inspector_name,
        "gps_lat": request.gps_lat,
        "gps_lon": request.gps_lon,
        "gps_accuracy": request.gps_accuracy,
        "description": request.description,
        "defects": [defect.dict() for defect in request.defects],
        "photos": [],
    }

    # Генерируем PDF
    pdf_bytes = document_service.generate_act_pdf(act_data)

    # Возвращаем PDF
    return StreamingResponse(
        io.BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=act_{request.act_number}_{datetime.now().strftime('%Y%m%d')}.pdf"
        },
    )


@router.post("/report/{inspection_id}", summary="Генерация отчета по проверке")
async def generate_inspection_report(
    inspection_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Генерация отчета по проверке

    - **inspection_id**: ID проверки
    """

    # Получаем проверку
    inspection = db.query(Inspection).filter(Inspection.id == inspection_id).first()
    if not inspection:
        raise HTTPException(status_code=404, detail="Проверка не найдена")

    # Получаем проект
    project = db.query(Project).filter(Project.id == inspection.project_id).first()

    # Подготавливаем данные
    report_data = {
        "id": inspection.id,
        "date": inspection.created_at.strftime("%d.%m.%Y"),
        "project_name": project.name if project else "—",
        "inspector_name": current_user.full_name,
        "status": inspection.status,
    }

    # Генерируем PDF
    pdf_bytes = document_service.generate_inspection_report(report_data)

    # Возвращаем PDF
    return StreamingResponse(
        io.BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=report_{inspection_id}_{datetime.now().strftime('%Y%m%d')}.pdf"
        },
    )


@router.post("/prescription", summary="Генерация предписания")
async def generate_prescription(
    inspection_id: int,
    text: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Генерация предписания об устранении нарушений

    - **inspection_id**: ID проверки
    - **text**: Текст предписания
    """

    # Получаем проверку
    inspection = db.query(Inspection).filter(Inspection.id == inspection_id).first()
    if not inspection:
        raise HTTPException(status_code=404, detail="Проверка не найдена")

    # Подготавливаем данные
    prescription_data = {
        "number": f"П-{inspection.id}/{datetime.now().year}",
        "date": datetime.now().strftime("%d.%m.%Y"),
        "text": text,
        "inspection_id": inspection.id,
    }

    # Генерируем PDF
    pdf_bytes = document_service.generate_prescription(prescription_data)

    # Возвращаем PDF
    return StreamingResponse(
        io.BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=prescription_{inspection.id}_{datetime.now().strftime('%Y%m%d')}.pdf"
        },
    )


@router.post("/watermark", summary="Добавление водяного знака на фото")
async def add_watermark(
    file: UploadFile = File(...),
    request: WatermarkRequest = Depends(),
    current_user: User = Depends(get_current_user),
):
    """
    Добавление водяного знака на фото

    - **file**: Файл изображения
    - **gps_lat**: Широта GPS (опционально)
    - **gps_lon**: Долгота GPS (опционально)
    - **project_name**: Название проекта (опционально)
    """

    # Проверяем формат файла
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Файл должен быть изображением")

    # Читаем файл
    image_bytes = await file.read()

    # Добавляем водяной знак
    watermarked_bytes = document_service.add_watermark_to_photo(
        image_bytes=image_bytes,
        gps_lat=request.gps_lat,
        gps_lon=request.gps_lon,
        timestamp=datetime.now(),
        project_name=request.project_name,
    )

    # Возвращаем изображение
    return StreamingResponse(
        io.BytesIO(watermarked_bytes),
        media_type="image/jpeg",
        headers={
            "Content-Disposition": f"attachment; filename=watermarked_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
        },
    )


@router.get("/templates", summary="Список доступных шаблонов")
async def list_templates(current_user: User = Depends(get_current_user)):
    """
    Получение списка доступных шаблонов документов
    """
    return {
        "templates": [
            {
                "id": "act_inspection",
                "name": "Акт освидетельствования скрытых работ",
                "description": "Стандартный акт освидетельствования",
                "format": "PDF",
            },
            {
                "id": "inspection_report",
                "name": "Отчет по проверке",
                "description": "Детальный отчет о проведенной проверке",
                "format": "PDF",
            },
            {
                "id": "prescription",
                "name": "Предписание",
                "description": "Предписание об устранении нарушений",
                "format": "PDF",
            },
            {
                "id": "project_summary",
                "name": "Сводный отчет по проекту",
                "description": "Общий отчет по всем проверкам проекта",
                "format": "PDF",
            },
        ]
    }
