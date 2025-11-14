"""
Модель нормативов (СП, ГОСТ и т.д.)
"""
from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean
from datetime import datetime
from app.database import Base


class Regulation(Base):
    """Модель норматива"""
    __tablename__ = "regulations"

    id = Column(Integer, primary_key=True, index=True)

    # Основная информация
    code = Column(String(100), unique=True, nullable=False, index=True)  # СП 63.13330.2018
    title = Column(String(1000), nullable=False)
    full_name = Column(Text, nullable=True)

    # Тип
    regulation_type = Column(String(50), nullable=False)  # СП, ГОСТ, СанПиН и т.д.

    # Содержание
    description = Column(Text, nullable=True)
    content = Column(Text, nullable=True)  # Полный текст или основные положения

    # Статус
    is_active = Column(Boolean, default=True)
    supersedes = Column(String(100), nullable=True)  # Какой документ заменяет
    superseded_by = Column(String(100), nullable=True)  # Каким документом заменен

    # Даты
    publication_date = Column(DateTime, nullable=True)
    effective_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Метаданные для поиска
    keywords = Column(Text, nullable=True)  # JSON массив ключевых слов
    categories = Column(Text, nullable=True)  # JSON массив категорий

    def __repr__(self):
        return f"<Regulation {self.code}>"
