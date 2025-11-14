"""
Модели чек-листов
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Boolean, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class ChecklistTemplate(Base):
    """Шаблон чек-листа"""
    __tablename__ = "checklist_templates"

    id = Column(Integer, primary_key=True, index=True)

    # Основная информация
    name = Column(String(500), nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String(255), nullable=True)  # Категория (фундамент, стены и т.д.)

    # Тип проекта, для которого подходит
    project_type = Column(String(100), nullable=True)
    construction_phase = Column(String(255), nullable=True)

    # Пункты шаблона (JSON)
    items_template = Column(Text, nullable=False)  # JSON массив с пунктами

    # Статус
    is_active = Column(Boolean, default=True)
    is_default = Column(Boolean, default=False)

    # Создатель
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)

    # Даты
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    checklists = relationship("Checklist", back_populates="template")

    def __repr__(self):
        return f"<ChecklistTemplate {self.name}>"


class Checklist(Base):
    """Чек-лист для конкретной проверки"""
    __tablename__ = "checklists"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    template_id = Column(Integer, ForeignKey("checklist_templates.id"), nullable=True)
    inspector_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Основная информация
    name = Column(String(500), nullable=False)
    description = Column(Text, nullable=True)

    # Локация
    floor_level = Column(String(50), nullable=True)
    section = Column(String(100), nullable=True)

    # Прогресс
    total_items = Column(Integer, default=0)
    completed_items = Column(Integer, default=0)
    completion_percentage = Column(Float, default=0.0)

    # Статус
    is_completed = Column(Boolean, default=False)
    completed_at = Column(DateTime, nullable=True)

    # Даты
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    project = relationship("Project", back_populates="checklists")
    template = relationship("ChecklistTemplate", back_populates="checklists")
    inspector = relationship("User")
    items = relationship("ChecklistItem", back_populates="checklist", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Checklist {self.name}>"


class ChecklistItem(Base):
    """Пункт чек-листа"""
    __tablename__ = "checklist_items"

    id = Column(Integer, primary_key=True, index=True)
    checklist_id = Column(Integer, ForeignKey("checklists.id"), nullable=False)

    # Содержание
    title = Column(String(500), nullable=False)
    description = Column(Text, nullable=True)
    order = Column(Integer, default=0)  # Порядок отображения

    # Требования
    is_required = Column(Boolean, default=False)
    requires_photo = Column(Boolean, default=False)
    regulation_reference = Column(String(500), nullable=True)  # Ссылка на норматив

    # Статус
    is_checked = Column(Boolean, default=False)
    is_compliant = Column(Boolean, nullable=True)  # Соответствует ли требованиям
    checked_at = Column(DateTime, nullable=True)
    checked_by = Column(Integer, ForeignKey("users.id"), nullable=True)

    # Комментарий и фото
    comment = Column(Text, nullable=True)
    photo_urls = Column(Text, nullable=True)  # JSON массив URL фотографий

    # Даты
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    checklist = relationship("Checklist", back_populates="items")

    def __repr__(self):
        return f"<ChecklistItem {self.title}>"
