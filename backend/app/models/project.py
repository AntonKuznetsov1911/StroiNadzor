"""
Модель проекта (объекта строительства)
"""
from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Text, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.database import Base


class ProjectType(str, enum.Enum):
    """Типы проектов"""
    RESIDENTIAL = "residential"  # Жилое
    COMMERCIAL = "commercial"    # Коммерческое
    INDUSTRIAL = "industrial"    # Промышленное
    INFRASTRUCTURE = "infrastructure"  # Инфраструктура
    RECONSTRUCTION = "reconstruction"  # Реконструкция


class ProjectStatus(str, enum.Enum):
    """Статусы проекта"""
    PLANNING = "planning"
    IN_PROGRESS = "in_progress"
    ON_HOLD = "on_hold"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Project(Base):
    """Модель проекта (объекта строительства)"""
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(500), nullable=False)
    description = Column(Text, nullable=True)
    project_type = Column(SQLEnum(ProjectType), nullable=False)
    status = Column(SQLEnum(ProjectStatus), default=ProjectStatus.PLANNING, nullable=False)

    # Адрес и геолокация
    address = Column(String(500), nullable=False)
    city = Column(String(255), nullable=True)
    region = Column(String(255), nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    # Даты
    start_date = Column(DateTime, nullable=True)
    planned_end_date = Column(DateTime, nullable=True)
    actual_end_date = Column(DateTime, nullable=True)

    # Прогресс
    completion_percentage = Column(Float, default=0.0)

    # Связи
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    created_by_user = relationship("User", back_populates="projects", foreign_keys=[created_by])
    inspections = relationship("Inspection", back_populates="project", cascade="all, delete-orphan")
    hidden_works = relationship("HiddenWork", back_populates="project", cascade="all, delete-orphan")
    checklists = relationship("Checklist", back_populates="project", cascade="all, delete-orphan")
    documents = relationship("Document", back_populates="project", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Project {self.name}>"
