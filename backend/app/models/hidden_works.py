"""
Модель контроля скрытых работ
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Boolean, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.database import Base


class HiddenWorkType(str, enum.Enum):
    """Типы скрытых работ"""
    FOUNDATION = "foundation"  # Фундамент
    REINFORCEMENT = "reinforcement"  # Армирование
    WATERPROOFING = "waterproofing"  # Гидроизоляция
    UTILITIES = "utilities"  # Коммуникации
    ELECTRICAL = "electrical"  # Электрика
    VENTILATION = "ventilation"  # Вентиляция
    OTHER = "other"


class HiddenWorkStatus(str, enum.Enum):
    """Статус скрытых работ"""
    PENDING = "pending"  # Ожидает осмотра
    IN_REVIEW = "in_review"  # На проверке
    APPROVED = "approved"  # Одобрено
    REJECTED = "rejected"  # Отклонено
    CLOSED = "closed"  # Закрыто


class HiddenWork(Base):
    """Модель скрытых работ"""
    __tablename__ = "hidden_works"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)

    # Основная информация
    title = Column(String(500), nullable=False)
    description = Column(Text, nullable=True)
    work_type = Column(SQLEnum(HiddenWorkType), nullable=False)
    status = Column(SQLEnum(HiddenWorkStatus), default=HiddenWorkStatus.PENDING, nullable=False)

    # Локация
    floor_level = Column(String(50), nullable=True)
    section = Column(String(100), nullable=True)
    axis = Column(String(100), nullable=True)  # Оси здания

    # Сроки
    planned_inspection_date = Column(DateTime, nullable=True)
    actual_inspection_date = Column(DateTime, nullable=True)
    closing_deadline = Column(DateTime, nullable=True)  # Дедлайн для закрытия работ

    # Уведомления
    notification_sent = Column(Boolean, default=False)
    notification_sent_at = Column(DateTime, nullable=True)

    # Даты
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    project = relationship("Project", back_populates="hidden_works")
    acts = relationship("HiddenWorkAct", back_populates="hidden_work", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<HiddenWork {self.title}>"


class HiddenWorkAct(Base):
    """Акт освидетельствования скрытых работ"""
    __tablename__ = "hidden_work_acts"

    id = Column(Integer, primary_key=True, index=True)
    hidden_work_id = Column(Integer, ForeignKey("hidden_works.id"), nullable=False)

    # Номер акта
    act_number = Column(String(100), unique=True, nullable=False)
    act_date = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Участники
    inspector_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    contractor_representative = Column(String(255), nullable=True)
    technical_supervision = Column(String(255), nullable=True)

    # Результаты
    is_approved = Column(Boolean, default=False)
    comments = Column(Text, nullable=True)
    defects_found = Column(Text, nullable=True)  # JSON список дефектов

    # Фотофиксация
    photos = Column(Text, nullable=True)  # JSON массив URL фотографий

    # Подписи (digital signatures)
    inspector_signature = Column(String(1000), nullable=True)
    contractor_signature = Column(String(1000), nullable=True)
    supervision_signature = Column(String(1000), nullable=True)

    # Документ
    document_url = Column(String(1000), nullable=True)  # Сгенерированный PDF

    # Даты
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    hidden_work = relationship("HiddenWork", back_populates="acts")
    inspector = relationship("User")

    def __repr__(self):
        return f"<HiddenWorkAct {self.act_number}>"
