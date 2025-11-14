"""
Модель проверок и фотофиксации
"""
from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Text, Boolean, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.database import Base


class InspectionStatus(str, enum.Enum):
    """Статус проверки"""
    DRAFT = "draft"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    APPROVED = "approved"
    REJECTED = "rejected"


class DefectSeverity(str, enum.Enum):
    """Степень критичности дефекта"""
    CRITICAL = "critical"  # Критический
    MAJOR = "major"        # Значительный
    MINOR = "minor"        # Незначительный
    COSMETIC = "cosmetic"  # Косметический


class DefectType(str, enum.Enum):
    """Типы дефектов"""
    CRACK = "crack"  # Трещины
    DEVIATION = "deviation"  # Отклонения
    REINFORCEMENT = "reinforcement"  # Проблемы с армированием
    WELDING = "welding"  # Дефекты сварки
    WATERPROOFING = "waterproofing"  # Гидроизоляция
    CONCRETE_QUALITY = "concrete_quality"  # Качество бетона
    OTHER = "other"


class Inspection(Base):
    """Модель проверки"""
    __tablename__ = "inspections"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    inspector_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Основная информация
    title = Column(String(500), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(SQLEnum(InspectionStatus), default=InspectionStatus.DRAFT, nullable=False)

    # Этап строительства
    construction_phase = Column(String(255), nullable=True)
    floor_level = Column(String(50), nullable=True)  # Этаж/уровень
    section = Column(String(100), nullable=True)  # Секция/корпус

    # Геолокация
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    # Даты
    inspection_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    project = relationship("Project", back_populates="inspections")
    inspector = relationship("User", back_populates="inspections", foreign_keys=[inspector_id])
    photos = relationship("InspectionPhoto", back_populates="inspection", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Inspection {self.title}>"


class InspectionPhoto(Base):
    """Модель фотофиксации"""
    __tablename__ = "inspection_photos"

    id = Column(Integer, primary_key=True, index=True)
    inspection_id = Column(Integer, ForeignKey("inspections.id"), nullable=False)

    # Файл
    file_url = Column(String(1000), nullable=False)
    thumbnail_url = Column(String(1000), nullable=True)
    file_size = Column(Integer, nullable=True)  # Размер в байтах

    # Метаданные
    caption = Column(String(500), nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    taken_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Водяной знак (метаданные для проверки подлинности)
    watermark_data = Column(Text, nullable=True)  # JSON с данными о фото

    # ИИ анализ
    ai_analyzed = Column(Boolean, default=False)
    ai_analysis_result = Column(Text, nullable=True)  # JSON с результатами анализа

    # Даты
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    inspection = relationship("Inspection", back_populates="photos")
    defects = relationship("DefectDetection", back_populates="photo", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<InspectionPhoto {self.id}>"


class DefectDetection(Base):
    """Обнаруженные дефекты (через ИИ или вручную)"""
    __tablename__ = "defect_detections"

    id = Column(Integer, primary_key=True, index=True)
    photo_id = Column(Integer, ForeignKey("inspection_photos.id"), nullable=False)

    # Тип и серьезность
    defect_type = Column(SQLEnum(DefectType), nullable=False)
    severity = Column(SQLEnum(DefectSeverity), nullable=False)

    # Описание
    description = Column(Text, nullable=True)
    recommendation = Column(Text, nullable=True)  # Рекомендации по устранению

    # Координаты на фото (для выделения области)
    bbox_x = Column(Float, nullable=True)  # Bounding box
    bbox_y = Column(Float, nullable=True)
    bbox_width = Column(Float, nullable=True)
    bbox_height = Column(Float, nullable=True)

    # Обнаружение
    detected_by_ai = Column(Boolean, default=False)
    confidence_score = Column(Float, nullable=True)  # Уверенность ИИ (0-1)

    # Статус устранения
    is_fixed = Column(Boolean, default=False)
    fixed_at = Column(DateTime, nullable=True)
    fix_verification_photo_url = Column(String(1000), nullable=True)

    # Даты
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    photo = relationship("InspectionPhoto", back_populates="defects")

    def __repr__(self):
        return f"<DefectDetection {self.defect_type}>"
