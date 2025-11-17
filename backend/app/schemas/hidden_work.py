"""
Pydantic схемы для скрытых работ
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime, date
from enum import Enum


class HiddenWorkType(str, Enum):
    """Типы скрытых работ"""
    FOUNDATION = "foundation"
    REINFORCEMENT = "reinforcement"
    WELDING = "welding"
    WATERPROOFING = "waterproofing"
    ELECTRICAL = "electrical"
    PLUMBING = "plumbing"
    HVAC = "hvac"


class HiddenWorkStatus(str, Enum):
    """Статусы скрытых работ"""
    PLANNED = "planned"
    IN_PROGRESS = "in_progress"
    AWAITING_INSPECTION = "awaiting_inspection"
    APPROVED = "approved"
    REJECTED = "rejected"
    COMPLETED = "completed"


# Base schemas
class HiddenWorkBase(BaseModel):
    """Базовая схема скрытых работ"""
    project_id: int
    work_type: HiddenWorkType
    description: str = Field(..., min_length=10, max_length=1000)
    location: str = Field(..., min_length=3, max_length=200)
    planned_date: Optional[date] = None
    notes: Optional[str] = Field(None, max_length=2000)


class HiddenWorkCreate(HiddenWorkBase):
    """Схема для создания скрытых работ"""
    pass


class HiddenWorkUpdate(BaseModel):
    """Схема для обновления скрытых работ"""
    work_type: Optional[HiddenWorkType] = None
    description: Optional[str] = Field(None, min_length=10, max_length=1000)
    location: Optional[str] = Field(None, min_length=3, max_length=200)
    planned_date: Optional[date] = None
    actual_date: Optional[date] = None
    status: Optional[HiddenWorkStatus] = None
    notes: Optional[str] = Field(None, max_length=2000)


class HiddenWorkResponse(HiddenWorkBase):
    """Схема ответа для скрытых работ"""
    id: int
    status: HiddenWorkStatus
    actual_date: Optional[date] = None
    created_at: datetime
    updated_at: datetime
    created_by_id: int

    # Связанные данные
    acts_count: int = 0

    class Config:
        from_attributes = True


# Акты освидетельствования
class HiddenWorkActBase(BaseModel):
    """Базовая схема акта освидетельствования"""
    act_number: str = Field(..., min_length=1, max_length=50)
    act_date: date
    work_description: str = Field(..., min_length=10, max_length=1000)
    materials_used: Optional[str] = Field(None, max_length=1000)
    executor_signature: Optional[str] = None
    inspector_signature: Optional[str] = None
    notes: Optional[str] = Field(None, max_length=2000)


class HiddenWorkActCreate(HiddenWorkActBase):
    """Схема для создания акта"""
    hidden_work_id: int


class HiddenWorkActUpdate(BaseModel):
    """Схема для обновления акта"""
    act_number: Optional[str] = Field(None, min_length=1, max_length=50)
    act_date: Optional[date] = None
    work_description: Optional[str] = Field(None, min_length=10, max_length=1000)
    materials_used: Optional[str] = Field(None, max_length=1000)
    executor_signature: Optional[str] = None
    inspector_signature: Optional[str] = None
    is_approved: Optional[bool] = None
    notes: Optional[str] = Field(None, max_length=2000)


class HiddenWorkActResponse(HiddenWorkActBase):
    """Схема ответа для акта"""
    id: int
    hidden_work_id: int
    is_approved: bool
    created_at: datetime
    created_by_id: int
    document_url: Optional[str] = None

    class Config:
        from_attributes = True


# Расширенные схемы с подробной информацией
class HiddenWorkDetail(HiddenWorkResponse):
    """Детальная информация о скрытых работах"""
    acts: List[HiddenWorkActResponse] = []
    project_name: Optional[str] = None
    creator_name: Optional[str] = None


class HiddenWorkList(BaseModel):
    """Список скрытых работ с пагинацией"""
    items: List[HiddenWorkResponse]
    total: int
    page: int
    page_size: int
    pages: int
