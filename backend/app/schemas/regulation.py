"""
Pydantic схемы для нормативных документов
"""
from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List
from datetime import datetime, date
from enum import Enum


class RegulationType(str, Enum):
    """Типы нормативных документов"""
    SP = "sp"  # Свод Правил
    GOST = "gost"  # ГОСТ
    SNIP = "snip"  # СНиП
    SANPIN = "sanpin"  # СанПиН
    PB = "pb"  # Правила безопасности
    RD = "rd"  # Руководящий документ
    OTHER = "other"


class RegulationCategory(str, Enum):
    """Категории нормативов"""
    CONSTRUCTION = "construction"
    SAFETY = "safety"
    FIRE_SAFETY = "fire_safety"
    SANITARY = "sanitary"
    ENVIRONMENTAL = "environmental"
    TECHNICAL = "technical"


# Base schemas
class RegulationBase(BaseModel):
    """Базовая схема норматива"""
    code: str = Field(..., min_length=3, max_length=50)
    title: str = Field(..., min_length=10, max_length=500)
    regulation_type: RegulationType
    category: RegulationCategory
    description: Optional[str] = Field(None, max_length=2000)
    effective_date: Optional[date] = None
    revision_date: Optional[date] = None


class RegulationCreate(RegulationBase):
    """Схема для создания норматива"""
    full_text: Optional[str] = None
    keywords: List[str] = Field(default_factory=list)
    related_regulations: List[str] = Field(default_factory=list)


class RegulationUpdate(BaseModel):
    """Схема для обновления норматива"""
    title: Optional[str] = Field(None, min_length=10, max_length=500)
    regulation_type: Optional[RegulationType] = None
    category: Optional[RegulationCategory] = None
    description: Optional[str] = Field(None, max_length=2000)
    effective_date: Optional[date] = None
    revision_date: Optional[date] = None
    full_text: Optional[str] = None
    keywords: Optional[List[str]] = None
    related_regulations: Optional[List[str]] = None
    is_active: Optional[bool] = None


class RegulationResponse(RegulationBase):
    """Схема ответа для норматива"""
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    # Дополнительные поля
    view_count: int = 0
    reference_count: int = 0

    class Config:
        from_attributes = True


class RegulationDetail(RegulationResponse):
    """Детальная информация о нормативе"""
    full_text: Optional[str] = None
    keywords: List[str] = []
    related_regulations: List[str] = []
    related_items: List['RegulationResponse'] = []


class RegulationList(BaseModel):
    """Список нормативов с пагинацией"""
    items: List[RegulationResponse]
    total: int
    page: int
    page_size: int
    pages: int


class RegulationSearch(BaseModel):
    """Схема для поиска нормативов"""
    query: str = Field(..., min_length=2, max_length=200)
    regulation_type: Optional[RegulationType] = None
    category: Optional[RegulationCategory] = None
    limit: int = Field(default=20, ge=1, le=100)


class RegulationSearchResult(BaseModel):
    """Результат поиска норматива"""
    id: int
    code: str
    title: str
    regulation_type: RegulationType
    category: RegulationCategory
    relevance_score: float = Field(..., ge=0.0, le=1.0)
    matched_keywords: List[str] = []
    excerpt: Optional[str] = None


class RegulationAIQuery(BaseModel):
    """Запрос к AI консультанту"""
    question: str = Field(..., min_length=10, max_length=1000)
    context: Optional[str] = Field(None, max_length=2000)
    regulation_ids: Optional[List[int]] = Field(default_factory=list)


class RegulationAIResponse(BaseModel):
    """Ответ от AI консультанта"""
    answer: str
    referenced_regulations: List[str] = []
    confidence: float = Field(..., ge=0.0, le=1.0)
    sources: List[RegulationResponse] = []
    model: Optional[str] = None
    tokens_used: Optional[int] = None
