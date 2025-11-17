"""
Pydantic схемы для документов
"""
from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List
from datetime import datetime
from enum import Enum


class DocumentType(str, Enum):
    """Типы документов"""
    TECHNICAL_SPEC = "technical_spec"
    BLUEPRINT = "blueprint"
    REPORT = "report"
    CERTIFICATE = "certificate"
    ACT = "act"
    PROTOCOL = "protocol"
    PHOTO = "photo"
    OTHER = "other"


class DocumentStatus(str, Enum):
    """Статусы документов"""
    DRAFT = "draft"
    UNDER_REVIEW = "under_review"
    APPROVED = "approved"
    REJECTED = "rejected"
    ARCHIVED = "archived"


# Base schemas
class DocumentBase(BaseModel):
    """Базовая схема документа"""
    title: str = Field(..., min_length=3, max_length=200)
    document_type: DocumentType
    description: Optional[str] = Field(None, max_length=1000)
    project_id: Optional[int] = None
    inspection_id: Optional[int] = None


class DocumentCreate(DocumentBase):
    """Схема для создания документа"""
    file_path: str = Field(..., min_length=1)
    file_size: int = Field(..., gt=0)
    mime_type: str = Field(..., min_length=1, max_length=100)


class DocumentUpdate(BaseModel):
    """Схема для обновления документа"""
    title: Optional[str] = Field(None, min_length=3, max_length=200)
    document_type: Optional[DocumentType] = None
    description: Optional[str] = Field(None, max_length=1000)
    status: Optional[DocumentStatus] = None
    version: Optional[int] = Field(None, gt=0)


class DocumentResponse(DocumentBase):
    """Схема ответа для документа"""
    id: int
    file_path: str
    file_size: int
    mime_type: str
    file_url: Optional[str] = None
    status: DocumentStatus
    version: int
    created_at: datetime
    updated_at: datetime
    uploaded_by_id: int

    # Метаданные
    download_count: int = 0
    is_public: bool = False

    class Config:
        from_attributes = True


class DocumentDetail(DocumentResponse):
    """Детальная информация о документе"""
    uploader_name: Optional[str] = None
    project_name: Optional[str] = None
    related_documents: List['DocumentResponse'] = []


class DocumentList(BaseModel):
    """Список документов с пагинацией"""
    items: List[DocumentResponse]
    total: int
    page: int
    page_size: int
    pages: int


class DocumentUpload(BaseModel):
    """Схема для загрузки документа"""
    title: str = Field(..., min_length=3, max_length=200)
    document_type: DocumentType
    description: Optional[str] = Field(None, max_length=1000)
    project_id: Optional[int] = None
    inspection_id: Optional[int] = None
    # file будет передан как multipart/form-data


class DocumentDownloadResponse(BaseModel):
    """Схема ответа для скачивания документа"""
    file_url: HttpUrl
    filename: str
    mime_type: str
    file_size: int
    expires_at: datetime
