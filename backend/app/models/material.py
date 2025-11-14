"""
Модели контроля материалов
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Boolean, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class Material(Base):
    """Модель материала на объекте"""
    __tablename__ = "materials"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)

    # Основная информация
    name = Column(String(500), nullable=False)
    category = Column(String(255), nullable=True)
    manufacturer = Column(String(255), nullable=True)
    supplier = Column(String(255), nullable=True)

    # Партия
    batch_number = Column(String(100), nullable=True)
    quantity = Column(Float, nullable=True)
    unit = Column(String(50), nullable=True)  # м3, тонн, шт и т.д.

    # Дата поставки
    delivery_date = Column(DateTime, nullable=True)

    # Хранение
    storage_location = Column(String(255), nullable=True)
    storage_conditions = Column(Text, nullable=True)

    # Статус проверки
    is_verified = Column(Boolean, default=False)
    verified_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    verified_at = Column(DateTime, nullable=True)

    # Комментарии
    notes = Column(Text, nullable=True)

    # Даты
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    certificates = relationship("MaterialCertificate", back_populates="material", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Material {self.name}>"


class MaterialCertificate(Base):
    """Сертификаты качества материалов"""
    __tablename__ = "material_certificates"

    id = Column(Integer, primary_key=True, index=True)
    material_id = Column(Integer, ForeignKey("materials.id"), nullable=False)

    # Информация о сертификате
    certificate_number = Column(String(255), nullable=False)
    certificate_type = Column(String(100), nullable=True)  # Паспорт, сертификат, декларация
    issuer = Column(String(255), nullable=True)
    issue_date = Column(DateTime, nullable=True)
    expiry_date = Column(DateTime, nullable=True)

    # Файл сертификата
    file_url = Column(String(1000), nullable=False)
    file_name = Column(String(500), nullable=False)

    # OCR данные
    ocr_extracted_data = Column(Text, nullable=True)  # JSON с извлеченными данными

    # Проверка подлинности
    is_verified = Column(Boolean, default=False)
    verification_method = Column(String(100), nullable=True)  # QR, база данных и т.д.
    verification_result = Column(Text, nullable=True)

    # Даты
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    material = relationship("Material", back_populates="certificates")

    def __repr__(self):
        return f"<MaterialCertificate {self.certificate_number}>"
