"""
Вспомогательные утилиты для обработки данных
"""
import re
import hashlib
import secrets
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta, date
from decimal import Decimal
import logging

logger = logging.getLogger(__name__)


def generate_unique_id(prefix: str = "") -> str:
    """
    Генерация уникального ID с опциональным префиксом

    Args:
        prefix: Префикс для ID (например, "PRJ", "INS", "DOC")

    Returns:
        Уникальный ID вида PREFIX-TIMESTAMP-RANDOM
    """
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    random_part = secrets.token_hex(4).upper()

    if prefix:
        return f"{prefix}-{timestamp}-{random_part}"
    return f"{timestamp}-{random_part}"


def calculate_hash(data: str, algorithm: str = "sha256") -> str:
    """
    Вычисление хеша строки

    Args:
        data: Данные для хеширования
        algorithm: Алгоритм хеширования (md5, sha1, sha256, sha512)

    Returns:
        Хеш строка
    """
    if algorithm == "md5":
        return hashlib.md5(data.encode()).hexdigest()
    elif algorithm == "sha1":
        return hashlib.sha1(data.encode()).hexdigest()
    elif algorithm == "sha256":
        return hashlib.sha256(data.encode()).hexdigest()
    elif algorithm == "sha512":
        return hashlib.sha512(data.encode()).hexdigest()
    else:
        raise ValueError(f"Unsupported hash algorithm: {algorithm}")


def format_file_size(size_bytes: int) -> str:
    """
    Форматирование размера файла в человекочитаемый вид

    Args:
        size_bytes: Размер в байтах

    Returns:
        Форматированная строка (например, "1.5 MB")
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} PB"


def parse_date_range(date_from: Optional[str], date_to: Optional[str]) -> tuple[Optional[date], Optional[date]]:
    """
    Парсинг диапазона дат из строк

    Args:
        date_from: Дата начала (YYYY-MM-DD)
        date_to: Дата окончания (YYYY-MM-DD)

    Returns:
        Tuple с датами начала и окончания
    """
    parsed_from = None
    parsed_to = None

    if date_from:
        try:
            parsed_from = datetime.strptime(date_from, "%Y-%m-%d").date()
        except ValueError as e:
            logger.warning(f"Invalid date_from format: {date_from}")

    if date_to:
        try:
            parsed_to = datetime.strptime(date_to, "%Y-%m-%d").date()
        except ValueError as e:
            logger.warning(f"Invalid date_to format: {date_to}")

    return parsed_from, parsed_to


def calculate_age_days(start_date: date) -> int:
    """
    Вычисление возраста в днях от указанной даты

    Args:
        start_date: Начальная дата

    Returns:
        Количество дней
    """
    return (datetime.now().date() - start_date).days


def calculate_completion_percentage(completed: int, total: int) -> float:
    """
    Вычисление процента завершения

    Args:
        completed: Количество завершенных элементов
        total: Общее количество элементов

    Returns:
        Процент завершения (0.0-100.0)
    """
    if total == 0:
        return 0.0
    return round((completed / total) * 100, 2)


def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """
    Обрезание текста до указанной длины

    Args:
        text: Исходный текст
        max_length: Максимальная длина
        suffix: Суффикс для добавления (обычно "...")

    Returns:
        Обрезанный текст
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def extract_numbers(text: str) -> List[float]:
    """
    Извлечение всех чисел из текста

    Args:
        text: Текст для обработки

    Returns:
        Список чисел
    """
    pattern = r'-?\d+\.?\d*'
    matches = re.findall(pattern, text)
    return [float(match) for match in matches]


def sanitize_filename(filename: str) -> str:
    """
    Очистка имени файла от недопустимых символов

    Args:
        filename: Исходное имя файла

    Returns:
        Очищенное имя файла
    """
    # Удаляем недопустимые символы
    sanitized = re.sub(r'[<>:"/\\|?*]', '_', filename)
    # Удаляем множественные подчеркивания
    sanitized = re.sub(r'_+', '_', sanitized)
    # Удаляем подчеркивания в начале и конце
    sanitized = sanitized.strip('_')

    return sanitized or "unnamed_file"


def create_pagination_metadata(
    total: int,
    page: int,
    page_size: int
) -> Dict[str, Any]:
    """
    Создание метаданных для пагинации

    Args:
        total: Общее количество элементов
        page: Текущая страница
        page_size: Размер страницы

    Returns:
        Словарь с метаданными пагинации
    """
    total_pages = (total + page_size - 1) // page_size  # Округление вверх

    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "pages": total_pages,
        "has_next": page < total_pages,
        "has_prev": page > 1
    }


def calculate_statistics(values: List[float]) -> Dict[str, float]:
    """
    Вычисление базовой статистики для списка значений

    Args:
        values: Список числовых значений

    Returns:
        Словарь со статистикой (min, max, avg, sum, count)
    """
    if not values:
        return {
            "min": 0.0,
            "max": 0.0,
            "avg": 0.0,
            "sum": 0.0,
            "count": 0
        }

    return {
        "min": min(values),
        "max": max(values),
        "avg": sum(values) / len(values),
        "sum": sum(values),
        "count": len(values)
    }


def group_by_date(
    items: List[Dict[str, Any]],
    date_field: str = "created_at"
) -> Dict[str, List[Dict[str, Any]]]:
    """
    Группировка элементов по дате

    Args:
        items: Список элементов
        date_field: Название поля с датой

    Returns:
        Словарь {дата: [элементы]}
    """
    grouped = {}

    for item in items:
        date_value = item.get(date_field)
        if isinstance(date_value, datetime):
            date_key = date_value.date().isoformat()
        elif isinstance(date_value, date):
            date_key = date_value.isoformat()
        else:
            date_key = "unknown"

        if date_key not in grouped:
            grouped[date_key] = []
        grouped[date_key].append(item)

    return grouped


def convert_decimal_to_float(obj: Any) -> Any:
    """
    Рекурсивное преобразование Decimal в float для JSON сериализации

    Args:
        obj: Объект для преобразования

    Returns:
        Объект с преобразованными Decimal значениями
    """
    if isinstance(obj, Decimal):
        return float(obj)
    elif isinstance(obj, dict):
        return {key: convert_decimal_to_float(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [convert_decimal_to_float(item) for item in obj]
    return obj


def merge_dicts_deep(dict1: Dict, dict2: Dict) -> Dict:
    """
    Глубокое слияние двух словарей

    Args:
        dict1: Первый словарь
        dict2: Второй словарь (приоритетный)

    Returns:
        Объединенный словарь
    """
    result = dict1.copy()

    for key, value in dict2.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = merge_dicts_deep(result[key], value)
        else:
            result[key] = value

    return result


def chunk_list(items: List[Any], chunk_size: int) -> List[List[Any]]:
    """
    Разбиение списка на чанки указанного размера

    Args:
        items: Исходный список
        chunk_size: Размер чанка

    Returns:
        Список чанков
    """
    return [items[i:i + chunk_size] for i in range(0, len(items), chunk_size)]


def calculate_expiry_status(expiry_date: Optional[date], warning_days: int = 30) -> str:
    """
    Определение статуса истечения срока

    Args:
        expiry_date: Дата истечения
        warning_days: Количество дней до истечения для предупреждения

    Returns:
        Статус: 'valid', 'expiring_soon', 'expired', 'no_expiry'
    """
    if not expiry_date:
        return "no_expiry"

    today = datetime.now().date()

    if expiry_date < today:
        return "expired"
    elif expiry_date <= today + timedelta(days=warning_days):
        return "expiring_soon"
    else:
        return "valid"


def format_currency(amount: Decimal, currency: str = "RUB") -> str:
    """
    Форматирование денежной суммы

    Args:
        amount: Сумма
        currency: Валюта (RUB, USD, EUR)

    Returns:
        Форматированная строка
    """
    symbols = {
        "RUB": "₽",
        "USD": "$",
        "EUR": "€"
    }

    symbol = symbols.get(currency, currency)
    formatted_amount = f"{amount:,.2f}"

    return f"{formatted_amount} {symbol}"
