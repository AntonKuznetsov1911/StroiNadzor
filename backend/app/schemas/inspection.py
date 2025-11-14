"""
Pydantic схемы для проверок и фотофиксации
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from app.models.inspection import InspectionStatus, DefectSeverity, DefectType


class InspectionPhotoCreate(BaseModel):
    """Схема для создания фото"""
    caption: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class InspectionPhotoResponse(BaseModel):
    """Схема ответа с данными фото"""
    id: int
    file_url: str
    thumbnail_url: Optional[str]
    caption: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    taken_at: datetime
    ai_analyzed: bool
    created_at: datetime

    class Config:
        from_attributes = True


class DefectDetectionCreate(BaseModel):
    """Схема для создания обнаружения дефекта"""
    defect_type: DefectType
    severity: DefectSeverity
    description: Optional[str] = None
    recommendation: Optional[str] = None


class DefectDetectionResponse(BaseModel):
    """Схема ответа с данными дефекта"""
    id: int
    defect_type: DefectType
    severity: DefectSeverity
    description: Optional[str]
    recommendation: Optional[str]
    detected_by_ai: bool
    confidence_score: Optional[float]
    is_fixed: bool
    created_at: datetime

    class Config:
        from_attributes = True


class InspectionBase(BaseModel):
    """Базовая схема проверки"""
    title: str = Field(..., min_length=3, max_length=500)
    description: Optional[str] = None
    construction_phase: Optional[str] = None
    floor_level: Optional[str] = None
    section: Optional[str] = None


class InspectionCreate(InspectionBase):
    """Схема для создания проверки"""
    project_id: int
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    inspection_date: Optional[datetime] = None


class InspectionUpdate(BaseModel):
    """Схема для обновления проверки"""
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[InspectionStatus] = None


class InspectionResponse(InspectionBase):
    """Схема ответа с данными проверки"""
    id: int
    project_id: int
    inspector_id: int
    status: InspectionStatus
    latitude: Optional[float]
    longitude: Optional[float]
    inspection_date: datetime
    created_at: datetime
    updated_at: datetime
    photos: List[InspectionPhotoResponse] = []

    class Config:
        from_attributes = True
