"""
Эндпоинты для работы с проверками и фотофиксацией (Модуль 1 MVP)
"""
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional
import os
import uuid
from datetime import datetime

from app.database import get_db
from app.models.user import User
from app.models.inspection import Inspection, InspectionPhoto, DefectDetection
from app.schemas.inspection import (
    InspectionCreate, InspectionUpdate, InspectionResponse,
    InspectionPhotoResponse, DefectDetectionCreate, DefectDetectionResponse
)
from app.api.v1.endpoints.auth import get_current_user

router = APIRouter()


@router.post("/", response_model=InspectionResponse, status_code=status.HTTP_201_CREATED)
async def create_inspection(
    inspection_data: InspectionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Создание новой проверки"""
    db_inspection = Inspection(
        **inspection_data.model_dump(),
        inspector_id=current_user.id
    )

    db.add(db_inspection)
    db.commit()
    db.refresh(db_inspection)

    return db_inspection


@router.get("/{inspection_id}", response_model=InspectionResponse)
async def get_inspection(
    inspection_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Получение проверки по ID"""
    inspection = db.query(Inspection).filter(Inspection.id == inspection_id).first()

    if not inspection:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Inspection not found"
        )

    return inspection


@router.post("/{inspection_id}/photos", response_model=InspectionPhotoResponse)
async def upload_inspection_photo(
    inspection_id: int,
    file: UploadFile = File(...),
    caption: Optional[str] = Form(None),
    latitude: Optional[float] = Form(None),
    longitude: Optional[float] = Form(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Загрузка фотографии для проверки
    С автоматической фиксацией даты, времени и GPS-координат
    """
    # Проверка существования проверки
    inspection = db.query(Inspection).filter(Inspection.id == inspection_id).first()
    if not inspection:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Inspection not found"
        )

    # Создание директории для загрузок
    upload_dir = f"uploads/inspections/{inspection_id}"
    os.makedirs(upload_dir, exist_ok=True)

    # Генерация уникального имени файла
    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(upload_dir, unique_filename)

    # Сохранение файла
    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)

    # Создание записи в БД
    db_photo = InspectionPhoto(
        inspection_id=inspection_id,
        file_url=f"/uploads/inspections/{inspection_id}/{unique_filename}",
        caption=caption,
        latitude=latitude,
        longitude=longitude,
        file_size=len(content),
        taken_at=datetime.utcnow()
    )

    db.add(db_photo)
    db.commit()
    db.refresh(db_photo)

    return db_photo


@router.post("/{inspection_id}/photos/{photo_id}/defects", response_model=DefectDetectionResponse)
async def create_defect_detection(
    inspection_id: int,
    photo_id: int,
    defect_data: DefectDetectionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Создание обнаружения дефекта (вручную)"""
    # Проверка существования фото
    photo = db.query(InspectionPhoto).filter(
        InspectionPhoto.id == photo_id,
        InspectionPhoto.inspection_id == inspection_id
    ).first()

    if not photo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Photo not found"
        )

    db_defect = DefectDetection(
        photo_id=photo_id,
        **defect_data.model_dump(),
        detected_by_ai=False
    )

    db.add(db_defect)
    db.commit()
    db.refresh(db_defect)

    return db_defect


@router.post("/{inspection_id}/analyze", response_model=InspectionResponse)
async def analyze_inspection_with_ai(
    inspection_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Анализ фотографий проверки с помощью ИИ для обнаружения дефектов
    TODO: Интеграция с ML моделью для распознавания дефектов
    """
    inspection = db.query(Inspection).filter(Inspection.id == inspection_id).first()

    if not inspection:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Inspection not found"
        )

    # Заглушка для ИИ анализа
    # В продакшене здесь будет вызов ML модели для анализа фотографий

    return inspection
