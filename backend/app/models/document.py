"""
Модель документов
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.database import Base


class DocumentType(str, enum.Enum):
    """Типы документов"""
    ACT = "act"  # Акт
    PROTOCOL = "protocol"  # Протокол
    REPORT = "report"  # Отчет
    PRESCRIPTION = "prescription"  # Предписание
    JOURNAL = "journal"  # Журнал
    EXECUTIVE = "executive"  # Исполнительная документация
    OTHER = "other"


class Document(Base):
    """Модель документа"""
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)

    # Основная информация
    title = Column(String(500), nullable=False)
    document_type = Column(SQLEnum(DocumentType), nullable=False)
    document_number = Column(String(100), nullable=True)

    # Файл
    file_url = Column(String(1000), nullable=False)
    file_name = Column(String(500), nullable=False)
    file_size = Column(Integer, nullable=True)
    mime_type = Column(String(100), nullable=True)

    # Метаданные
    description = Column(Text, nullable=True)
    tags = Column(Text, nullable=True)  # JSON массив тегов

    # Автор и дата
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    document_date = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Версионность
    version = Column(Integer, default=1)
    parent_document_id = Column(Integer, ForeignKey("documents.id"), nullable=True)

    # Даты
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    project = relationship("Project", back_populates="documents")
    creator = relationship("User")

    def __repr__(self):
        return f"<Document {self.title}>"
