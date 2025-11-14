"""
Pydantic схемы для проектов
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.models.project import ProjectType, ProjectStatus


class ProjectBase(BaseModel):
    """Базовая схема проекта"""
    name: str = Field(..., min_length=3, max_length=500)
    description: Optional[str] = None
    project_type: ProjectType
    address: str
    city: Optional[str] = None
    region: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class ProjectCreate(ProjectBase):
    """Схема для создания проекта"""
    start_date: Optional[datetime] = None
    planned_end_date: Optional[datetime] = None


class ProjectUpdate(BaseModel):
    """Схема для обновления проекта"""
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[ProjectStatus] = None
    completion_percentage: Optional[float] = Field(None, ge=0, le=100)
    planned_end_date: Optional[datetime] = None


class ProjectResponse(ProjectBase):
    """Схема ответа с данными проекта"""
    id: int
    status: ProjectStatus
    completion_percentage: float
    start_date: Optional[datetime]
    planned_end_date: Optional[datetime]
    actual_end_date: Optional[datetime]
    created_by: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ProjectListResponse(BaseModel):
    """Схема для списка проектов"""
    projects: list[ProjectResponse]
    total: int
    page: int
    page_size: int
