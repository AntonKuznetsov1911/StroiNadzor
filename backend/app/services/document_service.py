"""
Document Generation Service - Генерация актов освидетельствования скрытых работ

Функции:
- Генерация PDF актов освидетельствования
- Создание отчетов по проверкам
- Экспорт данных в различные форматы
- Добавление водяных знаков на фото
"""

import io
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Dict, Any
import logging

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image,
    PageBreak,
)
from reportlab.lib import colors
from PIL import Image as PILImage
from PIL import ImageDraw, ImageFont

logger = logging.getLogger(__name__)


class DocumentService:
    """Сервис для генерации документов и актов"""

    def __init__(self):
        self.page_width, self.page_height = A4
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()

    def _setup_custom_styles(self):
        """Настройка пользовательских стилей для PDF"""

        # Заголовок документа
        self.styles.add(
            ParagraphStyle(
                name="CustomTitle",
                parent=self.styles["Heading1"],
                fontSize=16,
                alignment=TA_CENTER,
                spaceAfter=12,
                fontName="Helvetica-Bold",
            )
        )

        # Подзаголовок
        self.styles.add(
            ParagraphStyle(
                name="CustomHeading",
                parent=self.styles["Heading2"],
                fontSize=14,
                alignment=TA_LEFT,
                spaceAfter=10,
                fontName="Helvetica-Bold",
            )
        )

        # Обычный текст
        self.styles.add(
            ParagraphStyle(
                name="CustomBody",
                parent=self.styles["Normal"],
                fontSize=11,
                alignment=TA_JUSTIFY,
                spaceAfter=6,
                leading=14,
            )
        )

        # Текст справа
        self.styles.add(
            ParagraphStyle(
                name="RightAlign",
                parent=self.styles["Normal"],
                fontSize=11,
                alignment=TA_RIGHT,
            )
        )

    def generate_act_pdf(self, act_data: Dict[str, Any]) -> bytes:
        """
        Генерация PDF акта освидетельствования (новая реализация)

        Args:
            act_data: Данные для акта
                - act_number: Номер акта
                - date: Дата
                - project_name: Название проекта
                - project_address: Адрес
                - customer: Заказчик
                - contractor: Подрядчик
                - work_type: Вид работ
                - inspector_name: Имя инспектора
                - gps_lat: Широта
                - gps_lon: Долгота
                - description: Описание
                - defects: Список дефектов
                - photos: Список фото

        Returns:
            bytes: PDF документ
        """
        logger.info(f"Generating inspection act PDF: {act_data.get('act_number')}")

        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=20 * mm,
            leftMargin=20 * mm,
            topMargin=20 * mm,
            bottomMargin=20 * mm,
        )

        story = []

        # Шапка
        story.append(Paragraph("АКТ ОСВИДЕТЕЛЬСТВОВАНИЯ", self.styles["CustomTitle"]))
        story.append(Paragraph("СКРЫТЫХ РАБОТ", self.styles["CustomTitle"]))
        story.append(Spacer(1, 10 * mm))

        # Номер и дата
        act_number = act_data.get("act_number", "б/н")
        act_date = act_data.get("date", datetime.now().strftime("%d.%m.%Y"))
        story.append(
            Paragraph(f"№ {act_number} от {act_date}", self.styles["RightAlign"])
        )
        story.append(Spacer(1, 8 * mm))

        # Основная информация
        story.append(Paragraph("1. ОБЩИЕ СВЕДЕНИЯ", self.styles["CustomHeading"]))

        info_data = [
            ["Наименование объекта:", act_data.get("project_name", "—")],
            ["Адрес объекта:", act_data.get("project_address", "—")],
            ["Заказчик:", act_data.get("customer", "—")],
            ["Подрядчик:", act_data.get("contractor", "—")],
            ["Вид работ:", act_data.get("work_type", "Скрытые работы")],
            ["Дата проверки:", act_date],
            ["Инспектор:", act_data.get("inspector_name", "—")],
        ]

        info_table = Table(info_data, colWidths=[70 * mm, 100 * mm])
        info_table.setStyle(
            TableStyle(
                [
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                    ("FONTSIZE", (0, 0), (-1, -1), 11),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ]
            )
        )
        story.append(info_table)
        story.append(Spacer(1, 8 * mm))

        # GPS координаты
        gps_lat = act_data.get("gps_lat")
        gps_lon = act_data.get("gps_lon")
        if gps_lat and gps_lon:
            story.append(Paragraph("2. ГЕОЛОКАЦИЯ", self.styles["CustomHeading"]))
            gps_text = (
                f"Широта: {gps_lat:.6f}°<br/>"
                f"Долгота: {gps_lon:.6f}°<br/>"
                f"Точность: ±{act_data.get('gps_accuracy', 10)} метров"
            )
            story.append(Paragraph(gps_text, self.styles["CustomBody"]))
            story.append(Spacer(1, 8 * mm))

        # Описание
        story.append(Paragraph("3. ОПИСАНИЕ РАБОТ", self.styles["CustomHeading"]))
        description = act_data.get(
            "description", "Проведено освидетельствование скрытых работ."
        )
        story.append(Paragraph(description, self.styles["CustomBody"]))
        story.append(Spacer(1, 8 * mm))

        # Дефекты
        defects = act_data.get("defects", [])
        if defects:
            story.append(
                Paragraph("4. ОБНАРУЖЕННЫЕ ДЕФЕКТЫ", self.styles["CustomHeading"])
            )

            defects_data = [["№", "Тип дефекта", "Уверенность", "Рекомендации"]]

            for idx, defect in enumerate(defects, 1):
                defects_data.append(
                    [
                        str(idx),
                        defect.get("name", "Неизвестно"),
                        f"{defect.get('confidence', 0):.1f}%",
                        defect.get("regulation", "—"),
                    ]
                )

            defects_table = Table(
                defects_data, colWidths=[10 * mm, 50 * mm, 30 * mm, 80 * mm]
            )
            defects_table.setStyle(
                TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                        ("FONTSIZE", (0, 0), (-1, 0), 11),
                        ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                        ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                        ("GRID", (0, 0), (-1, -1), 1, colors.black),
                        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                        ("FONTSIZE", (0, 1), (-1, -1), 10),
                    ]
                )
            )
            story.append(defects_table)
            story.append(Spacer(1, 8 * mm))
        else:
            story.append(
                Paragraph("4. ОБНАРУЖЕННЫЕ ДЕФЕКТЫ", self.styles["CustomHeading"])
            )
            story.append(
                Paragraph(
                    "Дефектов не обнаружено. Работы выполнены качественно.",
                    self.styles["CustomBody"],
                )
            )
            story.append(Spacer(1, 8 * mm))

        # Фото
        photos = act_data.get("photos", [])
        if photos:
            story.append(Paragraph("5. ФОТОФИКСАЦИЯ", self.styles["CustomHeading"]))
            story.append(
                Paragraph(
                    f"Прилагается {len(photos)} фотографий.",
                    self.styles["CustomBody"],
                )
            )

        # Заключение
        story.append(Spacer(1, 8 * mm))
        story.append(Paragraph("6. ЗАКЛЮЧЕНИЕ", self.styles["CustomHeading"]))

        if defects:
            conclusion = (
                f"По результатам освидетельствования скрытых работ обнаружено "
                f"{len(defects)} дефектов. Требуется устранение выявленных "
                f"несоответствий до продолжения работ."
            )
            story.append(Paragraph(conclusion, self.styles["CustomBody"]))
            story.append(Spacer(1, 5 * mm))
            story.append(
                Paragraph(
                    "<b>Работы не могут быть приняты до устранения дефектов.</b>",
                    self.styles["CustomBody"],
                )
            )
        else:
            conclusion = (
                "По результатам освидетельствования скрытых работ дефектов не обнаружено. "
                "Работы выполнены в соответствии с проектной документацией и требованиями "
                "строительных норм и правил. Работы могут быть приняты."
            )
            story.append(Paragraph(conclusion, self.styles["CustomBody"]))
            story.append(Spacer(1, 5 * mm))
            story.append(
                Paragraph(
                    "<b>Работы приняты. Разрешается производство последующих работ.</b>",
                    self.styles["CustomBody"],
                )
            )

        story.append(Spacer(1, 15 * mm))

        # Подписи
        story.append(Paragraph("ПОДПИСИ:", self.styles["CustomHeading"]))
        story.append(Spacer(1, 10 * mm))

        inspector_name = act_data.get("inspector_name", "")
        signatures_data = [
            ["Инспектор:", inspector_name, "_________________"],
            ["Представитель заказчика:", "", "_________________"],
            ["Представитель подрядчика:", "", "_________________"],
        ]

        signatures_table = Table(signatures_data, colWidths=[60 * mm, 60 * mm, 50 * mm])
        signatures_table.setStyle(
            TableStyle(
                [
                    ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                    ("FONTSIZE", (0, 0), (-1, -1), 11),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
                ]
            )
        )
        story.append(signatures_table)

        # Генерация
        doc.build(story)
        buffer.seek(0)

        logger.info("Inspection act PDF generated successfully")
        return buffer.getvalue()

    def add_watermark_to_photo(
        self,
        image_bytes: bytes,
        gps_lat: Optional[float] = None,
        gps_lon: Optional[float] = None,
        timestamp: Optional[datetime] = None,
        project_name: Optional[str] = None,
    ) -> bytes:
        """
        Добавление водяного знака на фото

        Args:
            image_bytes: Байты изображения
            gps_lat: Широта GPS
            gps_lon: Долгота GPS
            timestamp: Временная метка
            project_name: Название проекта

        Returns:
            bytes: Изображение с водяным знаком
        """
        logger.info("Adding watermark to photo")

        # Открываем изображение из байтов
        img = PILImage.open(io.BytesIO(image_bytes))

        # Создаем слой для рисования
        draw = ImageDraw.Draw(img)

        # Размер изображения
        width, height = img.size

        # Шрифт
        try:
            font_large = ImageFont.truetype("arial.ttf", 40)
            font_small = ImageFont.truetype("arial.ttf", 30)
        except:
            font_large = ImageFont.load_default()
            font_small = ImageFont.load_default()

        # Позиция для текста (внизу)
        y_position = height - 150

        # Полупрозрачный фон
        background_box = [(0, height - 160), (width, height)]
        draw.rectangle(background_box, fill=(0, 0, 0, 180))

        # Добавляем текст
        line_height = 35
        current_y = y_position

        # Проект
        if project_name:
            text = f"🏗️ {project_name}"
            draw.text((20, current_y), text, fill=(255, 255, 255), font=font_small)
            current_y += line_height

        # GPS
        if gps_lat and gps_lon:
            text = f"📍 GPS: {gps_lat:.6f}°, {gps_lon:.6f}°"
            draw.text((20, current_y), text, fill=(255, 255, 255), font=font_small)
            current_y += line_height

        # Дата и время
        if timestamp:
            text = f"🕐 {timestamp.strftime('%d.%m.%Y %H:%M:%S')}"
            draw.text((20, current_y), text, fill=(255, 255, 255), font=font_small)

        # Логотип в правом верхнем углу
        logo_text = "ТехНадзор"
        draw.text((width - 250, 20), logo_text, fill=(255, 255, 255, 200), font=font_large)

        # Сохраняем в BytesIO
        buffer = io.BytesIO()
        img.save(buffer, format="JPEG", quality=95)
        buffer.seek(0)

        logger.info("Watermark added successfully")
        return buffer.getvalue()

    def generate_inspection_report(self, inspection_data: Dict[str, Any]) -> bytes:
        """
        Генерация отчета по проверке

        Args:
            inspection_data: Данные проверки

        Returns:
            bytes: PDF отчет
        """
        logger.info(f"Generating inspection report: {inspection_data.get('id')}")

        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=20 * mm,
            leftMargin=20 * mm,
            topMargin=20 * mm,
            bottomMargin=20 * mm,
        )

        story = []

        # Заголовок
        story.append(
            Paragraph("ОТЧЕТ ПО ПРОВЕРКЕ", self.styles["CustomTitle"])
        )
        story.append(Spacer(1, 10 * mm))

        # Информация
        info = [
            ["Номер проверки:", str(inspection_data.get("id", "—"))],
            ["Дата:", inspection_data.get("date", "—")],
            ["Проект:", inspection_data.get("project_name", "—")],
            ["Инспектор:", inspection_data.get("inspector_name", "—")],
            ["Статус:", inspection_data.get("status", "—")],
        ]

        info_table = Table(info, colWidths=[70 * mm, 100 * mm])
        info_table.setStyle(
            TableStyle(
                [
                    ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                    ("FONTSIZE", (0, 0), (-1, -1), 11),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ]
            )
        )
        story.append(info_table)

        # Генерация
        doc.build(story)
        buffer.seek(0)

        logger.info("Inspection report generated successfully")
        return buffer.getvalue()

    def generate_prescription(self, prescription_data: Dict[str, Any]) -> bytes:
        """
        Генерация предписания об устранении нарушений

        Args:
            prescription_data: Данные для предписания

        Returns:
            bytes: PDF предписание
        """
        logger.info("Generating prescription document")

        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=20 * mm,
            leftMargin=20 * mm,
            topMargin=20 * mm,
            bottomMargin=20 * mm,
        )

        story = []

        # Заголовок
        story.append(
            Paragraph("ПРЕДПИСАНИЕ", self.styles["CustomTitle"])
        )
        story.append(
            Paragraph("ОБ УСТРАНЕНИИ НАРУШЕНИЙ", self.styles["CustomTitle"])
        )
        story.append(Spacer(1, 10 * mm))

        # Дата
        story.append(
            Paragraph(
                f"№ {prescription_data.get('number', 'б/н')} от {prescription_data.get('date', datetime.now().strftime('%d.%m.%Y'))}",
                self.styles["RightAlign"],
            )
        )
        story.append(Spacer(1, 8 * mm))

        # Основной текст
        story.append(
            Paragraph(
                prescription_data.get("text", "Выявлены нарушения требований строительных норм."),
                self.styles["CustomBody"],
            )
        )

        # Генерация
        doc.build(story)
        buffer.seek(0)

        logger.info("Prescription document generated successfully")
        return buffer.getvalue()

    def export_to_word(self, data: Dict[str, Any], template: str) -> str:
        """
        Экспорт данных в Word документ

        Args:
            data: Данные для экспорта
            template: Путь к шаблону Word

        Returns:
            Путь к созданному документу
        """
        logger.info(f"Exporting to Word using template: {template}")

        # TODO: Интеграция с python-docx
        filename = f"export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx"
        filepath = f"/uploads/exports/{filename}"

        return filepath


# Singleton instance
document_service = DocumentService()
