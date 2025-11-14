"""
Утилиты валидации
"""
import re
from typing import Optional


def validate_phone(phone: str) -> bool:
    """
    Валидация российского номера телефона

    Args:
        phone: Номер телефона

    Returns:
        True если валидный
    """
    # Простой паттерн для российских номеров
    pattern = r'^(\+7|7|8)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$'
    return bool(re.match(pattern, phone))


def validate_email(email: str) -> bool:
    """Валидация email"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_coordinates(latitude: float, longitude: float) -> bool:
    """
    Валидация GPS координат

    Args:
        latitude: Широта (-90 до 90)
        longitude: Долгота (-180 до 180)

    Returns:
        True если валидные
    """
    return -90 <= latitude <= 90 and -180 <= longitude <= 180


def sanitize_filename(filename: str) -> str:
    """
    Очистка имени файла от опасных символов

    Args:
        filename: Исходное имя файла

    Returns:
        Безопасное имя файла
    """
    # Удаляем опасные символы
    filename = re.sub(r'[^\w\s\-\.]', '', filename)

    # Ограничиваем длину
    if len(filename) > 255:
        name, ext = filename.rsplit('.', 1) if '.' in filename else (filename, '')
        filename = name[:250] + ('.' + ext if ext else '')

    return filename
