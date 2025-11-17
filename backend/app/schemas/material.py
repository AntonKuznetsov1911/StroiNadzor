"""
Pydantic схемы для материалов и сертификатов
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime, date
from decimal import Decimal


# Материалы
class MaterialBase(BaseModel):
    """Базовая схема материала"""
    name: str = Field(..., min_length=3, max_length=200)
    category: str = Field(..., min_length=2, max_length=100)
    manufacturer: Optional[str] = Field(None, max_length=200)
    specification: Optional[str] = Field(None, max_length=500)
    unit: str = Field(..., max_length=20)  # м3, т, шт и т.д.


class MaterialCreate(MaterialBase):
    """Схема для создания материала"""
    project_id: int
    quantity: Decimal = Field(..., gt=0, decimal_places=3)
    unit_price: Optional[Decimal] = Field(None, ge=0, decimal_places=2)
    supplier: Optional[str] = Field(None, max_length=200)
    delivery_date: Optional[date] = None
    notes: Optional[str] = Field(None, max_length=1000)


class MaterialUpdate(BaseModel):
    """Схема для обновления материала"""
    name: Optional[str] = Field(None, min_length=3, max_length=200)
    category: Optional[str] = Field(None, min_length=2, max_length=100)
    manufacturer: Optional[str] = Field(None, max_length=200)
    specification: Optional[str] = Field(None, max_length=500)
    quantity: Optional[Decimal] = Field(None, gt=0, decimal_places=3)
    unit_price: Optional[Decimal] = Field(None, ge=0, decimal_places=2)
    supplier: Optional[str] = Field(None, max_length=200)
    delivery_date: Optional[date] = None
    notes: Optional[str] = Field(None, max_length=1000)


class MaterialResponse(MaterialBase):
    """Схема ответа для материала"""
    id: int
    project_id: int
    quantity: Decimal
    unit_price: Optional[Decimal] = None
    total_price: Optional[Decimal] = None
    supplier: Optional[str] = None
    delivery_date: Optional[date] = None
    notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    # Связанные данные
    certificates_count: int = 0
    has_valid_certificate: bool = False

    class Config:
        from_attributes = True


# Сертификаты
class MaterialCertificateBase(BaseModel):
    """Базовая схема сертификата"""
    certificate_number: str = Field(..., min_length=3, max_length=100)
    certificate_type: str = Field(..., min_length=2, max_length=100)
    issuing_authority: str = Field(..., min_length=3, max_length=200)
    issue_date: date
    expiry_date: Optional[date] = None


class MaterialCertificateCreate(MaterialCertificateBase):
    """Схема для создания сертификата"""
    material_id: int
    document_url: Optional[str] = None
    notes: Optional[str] = Field(None, max_length=1000)


class MaterialCertificateUpdate(BaseModel):
    """Схема для обновления сертификата"""
    certificate_number: Optional[str] = Field(None, min_length=3, max_length=100)
    certificate_type: Optional[str] = Field(None, min_length=2, max_length=100)
    issuing_authority: Optional[str] = Field(None, min_length=3, max_length=200)
    issue_date: Optional[date] = None
    expiry_date: Optional[date] = None
    document_url: Optional[str] = None
    notes: Optional[str] = Field(None, max_length=1000)
    is_valid: Optional[bool] = None


class MaterialCertificateResponse(MaterialCertificateBase):
    """Схема ответа для сертификата"""
    id: int
    material_id: int
    document_url: Optional[str] = None
    notes: Optional[str] = None
    is_valid: bool
    created_at: datetime
    uploaded_by_id: int

    class Config:
        from_attributes = True


# Расширенные схемы
class MaterialDetail(MaterialResponse):
    """Детальная информация о материале"""
    certificates: List[MaterialCertificateResponse] = []
    project_name: Optional[str] = None


class MaterialList(BaseModel):
    """Список материалов с пагинацией"""
    items: List[MaterialResponse]
    total: int
    page: int
    page_size: int
    pages: int


class MaterialStatistics(BaseModel):
    """Статистика по материалам"""
    total_materials: int
    total_quantity: Decimal
    total_value: Decimal
    materials_with_certificates: int
    expired_certificates: int
    expiring_soon_certificates: int
    categories: List[dict] = []
    top_suppliers: List[dict] = []


class MaterialInventory(BaseModel):
    """Инвентаризация материалов"""
    material_id: int
    material_name: str
    category: str
    planned_quantity: Decimal
    delivered_quantity: Decimal
    used_quantity: Decimal
    remaining_quantity: Decimal
    unit: str
    status: str  # sufficient, low, depleted
