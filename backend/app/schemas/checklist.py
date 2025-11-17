"""
Pydantic схемы для чек-листов
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class ChecklistStatus(str, Enum):
    """Статусы чек-листа"""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class CheckItemStatus(str, Enum):
    """Статусы пункта чек-листа"""
    PENDING = "pending"
    PASS = "pass"
    FAIL = "fail"
    NA = "na"  # Not Applicable


class Priority(str, Enum):
    """Приоритет"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


# Шаблоны чек-листов
class ChecklistTemplateItemBase(BaseModel):
    """Базовая схема пункта шаблона"""
    title: str = Field(..., min_length=3, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    order: int = Field(..., ge=1)
    is_mandatory: bool = True
    priority: Priority = Priority.MEDIUM


class ChecklistTemplateItemCreate(ChecklistTemplateItemBase):
    """Схема для создания пункта шаблона"""
    pass


class ChecklistTemplateItemResponse(ChecklistTemplateItemBase):
    """Схема ответа для пункта шаблона"""
    id: int
    template_id: int

    class Config:
        from_attributes = True


class ChecklistTemplateBase(BaseModel):
    """Базовая схема шаблона чек-листа"""
    name: str = Field(..., min_length=3, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    category: str = Field(..., min_length=2, max_length=100)


class ChecklistTemplateCreate(ChecklistTemplateBase):
    """Схема для создания шаблона"""
    items: List[ChecklistTemplateItemCreate] = []


class ChecklistTemplateUpdate(BaseModel):
    """Схема для обновления шаблона"""
    name: Optional[str] = Field(None, min_length=3, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    category: Optional[str] = Field(None, min_length=2, max_length=100)
    is_active: Optional[bool] = None


class ChecklistTemplateResponse(ChecklistTemplateBase):
    """Схема ответа для шаблона"""
    id: int
    is_active: bool
    created_at: datetime
    created_by_id: int
    items_count: int = 0

    class Config:
        from_attributes = True


class ChecklistTemplateDetail(ChecklistTemplateResponse):
    """Детальная информация о шаблоне"""
    items: List[ChecklistTemplateItemResponse] = []


# Чек-листы
class ChecklistItemBase(BaseModel):
    """Базовая схема пункта чек-листа"""
    title: str = Field(..., min_length=3, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    order: int = Field(..., ge=1)
    is_mandatory: bool = True
    priority: Priority = Priority.MEDIUM


class ChecklistItemCreate(ChecklistItemBase):
    """Схема для создания пункта чек-листа"""
    pass


class ChecklistItemUpdate(BaseModel):
    """Схема для обновления пункта"""
    status: Optional[CheckItemStatus] = None
    checked_at: Optional[datetime] = None
    checked_by_id: Optional[int] = None
    notes: Optional[str] = Field(None, max_length=1000)
    photo_url: Optional[str] = None


class ChecklistItemResponse(ChecklistItemBase):
    """Схема ответа для пункта чек-листа"""
    id: int
    checklist_id: int
    status: CheckItemStatus
    checked_at: Optional[datetime] = None
    checked_by_id: Optional[int] = None
    notes: Optional[str] = None
    photo_url: Optional[str] = None

    class Config:
        from_attributes = True


class ChecklistBase(BaseModel):
    """Базовая схема чек-листа"""
    project_id: int
    inspection_id: Optional[int] = None
    name: str = Field(..., min_length=3, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)


class ChecklistCreate(ChecklistBase):
    """Схема для создания чек-листа"""
    template_id: Optional[int] = None
    items: List[ChecklistItemCreate] = []


class ChecklistUpdate(BaseModel):
    """Схема для обновления чек-листа"""
    name: Optional[str] = Field(None, min_length=3, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    status: Optional[ChecklistStatus] = None


class ChecklistResponse(ChecklistBase):
    """Схема ответа для чек-листа"""
    id: int
    status: ChecklistStatus
    created_at: datetime
    updated_at: datetime
    created_by_id: int

    # Статистика
    total_items: int = 0
    completed_items: int = 0
    failed_items: int = 0
    completion_percentage: float = 0.0

    class Config:
        from_attributes = True


class ChecklistDetail(ChecklistResponse):
    """Детальная информация о чек-листе"""
    items: List[ChecklistItemResponse] = []
    project_name: Optional[str] = None
    creator_name: Optional[str] = None


class ChecklistList(BaseModel):
    """Список чек-листов с пагинацией"""
    items: List[ChecklistResponse]
    total: int
    page: int
    page_size: int
    pages: int


class ChecklistStatistics(BaseModel):
    """Статистика по чек-листам"""
    total_checklists: int
    completed_checklists: int
    in_progress_checklists: int
    failed_checklists: int
    average_completion_rate: float
    total_items: int
    passed_items: int
    failed_items: int
