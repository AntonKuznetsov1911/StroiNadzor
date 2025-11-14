"""
Утилиты для создания водяных знаков на фотографиях
"""
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
from typing import Optional
import io
import logging

logger = logging.getLogger(__name__)


def add_watermark(
    image_data: bytes,
    text: str,
    position: str = "bottom_right",
    font_size: int = 20,
    opacity: int = 180
) -> bytes:
    """
    Добавление водяного знака на изображение

    Args:
        image_data: Бинарные данные изображения
        text: Текст водяного знака
        position: Позиция (bottom_right, bottom_left, top_right, top_left)
        font_size: Размер шрифта
        opacity: Прозрачность (0-255)

    Returns:
        Изображение с водяным знаком в виде bytes
    """
    try:
        # Открываем изображение
        image = Image.open(io.BytesIO(image_data))

        # Создаем слой для водяного знака
        watermark = Image.new('RGBA', image.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(watermark)

        # Пытаемся использовать системный шрифт
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = ImageFont.load_default()

        # Получаем размеры текста
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        # Определяем позицию
        margin = 10
        if position == "bottom_right":
            x = image.width - text_width - margin
            y = image.height - text_height - margin
        elif position == "bottom_left":
            x = margin
            y = image.height - text_height - margin
        elif position == "top_right":
            x = image.width - text_width - margin
            y = margin
        else:  # top_left
            x = margin
            y = margin

        # Рисуем фон для текста
        padding = 5
        draw.rectangle(
            [x - padding, y - padding, x + text_width + padding, y + text_height + padding],
            fill=(0, 0, 0, opacity // 2)
        )

        # Рисуем текст
        draw.text((x, y), text, fill=(255, 255, 255, opacity), font=font)

        # Объединяем изображения
        if image.mode != 'RGBA':
            image = image.convert('RGBA')

        watermarked = Image.alpha_composite(image, watermark)

        # Конвертируем обратно в RGB если нужно
        if watermarked.mode == 'RGBA':
            watermarked = watermarked.convert('RGB')

        # Сохраняем в bytes
        output = io.BytesIO()
        watermarked.save(output, format='JPEG', quality=95)
        output.seek(0)

        return output.read()

    except Exception as e:
        logger.error(f"Error adding watermark: {str(e)}")
        raise


def create_inspection_watermark(
    project_name: str,
    date: datetime,
    latitude: Optional[float] = None,
    longitude: Optional[float] = None,
    inspector_name: Optional[str] = None
) -> str:
    """
    Создание текста водяного знака для фотофиксации

    Returns:
        Форматированный текст для водяного знака
    """
    lines = [
        project_name,
        date.strftime("%d.%m.%Y %H:%M:%S")
    ]

    if latitude and longitude:
        lines.append(f"GPS: {latitude:.6f}, {longitude:.6f}")

    if inspector_name:
        lines.append(f"Инженер: {inspector_name}")

    return "\n".join(lines)
