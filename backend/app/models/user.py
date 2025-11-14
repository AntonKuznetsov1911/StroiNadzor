"""
Модель пользователя
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.database import Base


class UserRole(str, enum.Enum):
    """Роли пользователей"""
    ADMIN = "admin"
    ENGINEER = "engineer"
    SUPERVISOR = "supervisor"
    CONTRACTOR = "contractor"
    VIEWER = "viewer"


class User(Base):
    """Модель пользователя"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    phone = Column(String(20), unique=True, nullable=True)
    full_name = Column(String(255), nullable=False)
    position = Column(String(255), nullable=True)
    hashed_password = Column(String(255), nullable=False)
    role = Column(SQLEnum(UserRole), default=UserRole.ENGINEER, nullable=False)

    # Профиль
    avatar_url = Column(String(500), nullable=True)
    company = Column(String(255), nullable=True)
    certificates = Column(String(1000), nullable=True)  # JSON строка с сертификатами

    # Статус
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)

    # Даты
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)

    # Связи
    projects = relationship("Project", back_populates="created_by_user", foreign_keys="Project.created_by")
    inspections = relationship("Inspection", back_populates="inspector", foreign_keys="Inspection.inspector_id")

    def __repr__(self):
        return f"<User {self.email}>"
