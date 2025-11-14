"""
AI Consultant Service V2 - Улучшенный профессиональный консультант

✨ НОВОЕ:
- Структурированный формат ответов (введение, детали, примеры, нормативы)
- Расширенная база знаний: кровля, изоляция, вентиляция
- Метаданные: уровень сложности, время чтения, ключевые термины
- Таблицы, расчеты, практические примеры
"""

import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class ComplexityLevel(str, Enum):
    """Уровень сложности темы"""
    BASIC = "Начальный"
    INTERMEDIATE = "Средний"
    ADVANCED = "Продвинутый"
    EXPERT = "Экспертный"


class KnowledgeItem:
    """Элемент базы знаний с метаданными"""

    def __init__(
        self,
        topic: str,
        keywords: List[str],
        regulations: List[str],
        content: str,
        complexity: ComplexityLevel,
        reading_time_minutes: int,
        key_terms: List[str],
        related_topics: List[str] = None
    ):
        self.topic = topic
        self.keywords = keywords
        self.regulations = regulations
        self.content = content
        self.complexity = complexity
        self.reading_time_minutes = reading_time_minutes
        self.key_terms = key_terms
        self.related_topics = related_topics or []

    def to_dict(self) -> Dict[str, Any]:
        """Преобразовать в словарь"""
        return {
            "topic": self.topic,
            "keywords": self.keywords,
            "regulations": self.regulations,
            "content": self.content,
            "metadata": {
                "complexity": self.complexity.value,
                "reading_time_minutes": self.reading_time_minutes,
                "key_terms": self.key_terms,
                "related_topics": self.related_topics
            }
        }


class AIConsultantServiceV2:
    """Улучшенный сервис AI консультанта"""

    def __init__(self):
        self.regulations_db = self._load_regulations_database()
        self.knowledge_base = self._build_enhanced_knowledge_base()

    def _load_regulations_database(self) -> Dict[str, Any]:
        """Загрузка базы данных нормативов"""
        try:
            db_path = Path(__file__).parent.parent.parent / "data" / "regulations_database.json"
            with open(db_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading regulations database: {e}")
            return {"regulations": [], "defect_categories": []}

    def _format_structured_response(
        self,
        title: str,
        introduction: str,
        details: str,
        examples: str,
        regulations_section: str,
        metadata: Dict[str, Any]
    ) -> str:
        """
        Форматирование структурированного ответа

        Args:
            title: Заголовок
            introduction: Введение/обзор
            details: Детальная информация
            examples: Практические примеры
            regulations_section: Ссылки на нормативы
            metadata: Метаданные (сложность, время, термины)

        Returns:
            Отформатированный HTML ответ
        """

        # Метаданные в виде бейджей
        complexity_badge = {
            "Начальный": "🟢",
            "Средний": "🟡",
            "Продвинутый": "🟠",
            "Экспертный": "🔴"
        }.get(metadata["complexity"], "⚪")

        metadata_section = f"""
<div style="background: #f8f9fa; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
    <strong>📊 Информация о материале:</strong><br>
    {complexity_badge} <strong>Уровень сложности:</strong> {metadata["complexity"]}<br>
    ⏱️ <strong>Время чтения:</strong> {metadata["reading_time_minutes"]} мин<br>
    🏷️ <strong>Ключевые термины:</strong> {", ".join(metadata["key_terms"][:5])}
</div>
"""

        return f"""
<div style="max-width: 900px; font-family: Arial, sans-serif;">

    <h1 style="color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px;">
        {title}
    </h1>

    {metadata_section}

    <section style="margin: 20px 0;">
        <h2 style="color: #34495e;">📋 Введение</h2>
        <div style="background: #ecf0f1; padding: 15px; border-left: 4px solid #3498db;">
            {introduction}
        </div>
    </section>

    <section style="margin: 20px 0;">
        <h2 style="color: #34495e;">🔍 Детальная информация</h2>
        {details}
    </section>

    <section style="margin: 20px 0;">
        <h2 style="color: #34495e;">💡 Практические примеры</h2>
        {examples}
    </section>

    <section style="margin: 20px 0;">
        <h2 style="color: #34495e;">📚 Нормативные документы</h2>
        <div style="background: #fff3cd; padding: 15px; border-radius: 8px;">
            {regulations_section}
        </div>
    </section>

</div>
"""

    def _build_enhanced_knowledge_base(self) -> Dict[str, KnowledgeItem]:
        """Построение расширенной базы знаний с новыми темами"""

        knowledge = {}

        # ============ НОВАЯ ТЕМА: КРОВЛЯ ============
        knowledge["кровля"] = KnowledgeItem(
            topic="Кровля и кровельные работы",
            keywords=["кровля", "крыша", "покрытие", "гидроизоляция кровли", "мягкая кровля", "металлочерепица", "roof"],
            regulations=["СП 17.13330.2017", "СП 71.13330.2017", "ГОСТ 30547-97"],
            complexity=ComplexityLevel.INTERMEDIATE,
            reading_time_minutes=12,
            key_terms=[
                "пароизоляция", "гидроизоляция", "контробрешетка", "мауэрлат",
                "стропильная система", "уклон кровли", "снеговая нагрузка"
            ],
            related_topics=["гидроизоляция", "теплоизоляция", "вентиляция"],
            content=self._get_roofing_content()
        )

        # ============ НОВАЯ ТЕМА: ТЕПЛОИЗОЛЯЦИЯ ============
        knowledge["теплоизоляция"] = KnowledgeItem(
            topic="Теплоизоляция зданий",
            keywords=["теплоизоляция", "утепление", "утеплитель", "минвата", "пенополистирол", "insulation"],
            regulations=["СП 50.13330.2012", "СП 23-101-2004", "ГОСТ 30494-2011"],
            complexity=ComplexityLevel.INTERMEDIATE,
            reading_time_minutes=10,
            key_terms=[
                "коэффициент теплопроводности", "теплов

ое сопротивление",
                "точка росы", "паропроницаемость", "теплоэффективность"
            ],
            related_topics=["вентиляция", "энергосбережение", "кровля"],
            content=self._get_insulation_content()
        )

        # ============ НОВАЯ ТЕМА: ВЕНТИЛЯЦИЯ ============
        knowledge["вентиляция"] = KnowledgeItem(
            topic="Вентиляция и кондиционирование",
            keywords=["вентиляция", "проветривание", "приточная", "вытяжная", "рекуперация", "ventilation"],
            regulations=["СП 60.13330.2020", "ГОСТ 30494-2011", "СНиП 41-01-2003"],
            complexity=ComplexityLevel.ADVANCED,
            reading_time_minutes=15,
            key_terms=[
                "воздухообмен", "кратность", "рекуперация тепла",
                "приток", "вытяжка", "аэродинамика"
            ],
            related_topics=["теплоизоляция", "энергосбережение", "комфорт"],
            content=self._get_ventilation_content()
        )

        return knowledge

    def _get_roofing_content(self) -> str:
        """Контент по кровельным работам"""
        return """
<strong>📋 ВВЕДЕНИЕ</strong><br>
Кровля - верхняя ограждающая конструкция здания, защищающая от атмосферных осадков, ветра, солнечной радиации. Правильное устройство кровли критически важно для долговечности здания.<br><br>

<strong>🔍 ДЕТАЛЬНАЯ ИНФОРМАЦИЯ</strong><br><br>

<strong>1. ТИПЫ КРОВЕЛЬНЫХ ПОКРЫТИЙ (СП 17.13330.2017)</strong><br><br>

<table style="width:100%; border-collapse: collapse; margin: 15px 0;">
    <tr style="background: #3498db; color: white;">
        <th style="padding: 10px; border: 1px solid #ddd;">Тип покрытия</th>
        <th style="padding: 10px; border: 1px solid #ddd;">Срок службы</th>
        <th style="padding: 10px; border: 1px solid #ddd;">Мин. уклон</th>
        <th style="padding: 10px; border: 1px solid #ddd;">Применение</th>
    </tr>
    <tr>
        <td style="padding: 10px; border: 1px solid #ddd;"><strong>Металлочерепица</strong></td>
        <td style="padding: 10px; border: 1px solid #ddd;">30-50 лет</td>
        <td style="padding: 10px; border: 1px solid #ddd;">14° (25%)</td>
        <td style="padding: 10px; border: 1px solid #ddd;">Скатные кровли жилых домов</td>
    </tr>
    <tr style="background: #f8f9fa;">
        <td style="padding: 10px; border: 1px solid #ddd;"><strong>Гибкая черепица</strong></td>
        <td style="padding: 10px; border: 1px solid #ddd;">20-30 лет</td>
        <td style="padding: 10px; border: 1px solid #ddd;">11° (20%)</td>
        <td style="padding: 10px; border: 1px solid #ddd;">Сложные формы, коттеджи</td>
    </tr>
    <tr>
        <td style="padding: 10px; border: 1px solid #ddd;"><strong>Профнастил</strong></td>
        <td style="padding: 10px; border: 1px solid #ddd;">25-40 лет</td>
        <td style="padding: 10px; border: 1px solid #ddd;">10° (18%)</td>
        <td style="padding: 10px; border: 1px solid #ddd;">Промышленные здания</td>
    </tr>
    <tr style="background: #f8f9fa;">
        <td style="padding: 10px; border: 1px solid #ddd;"><strong>ПВХ-мембрана</strong></td>
        <td style="padding: 10px; border: 1px solid #ddd;">30-50 лет</td>
        <td style="padding: 10px; border: 1px solid #ddd;">0° (плоская)</td>
        <td style="padding: 10px; border: 1px solid #ddd;">Плоские кровли</td>
    </tr>
    <tr>
        <td style="padding: 10px; border: 1px solid #ddd;"><strong>Наплавляемая</strong></td>
        <td style="padding: 10px; border: 1px solid #ddd;">15-25 лет</td>
        <td style="padding: 10px; border: 1px solid #ddd;">0-3°</td>
        <td style="padding: 10px; border: 1px solid #ddd;">Плоские кровли жилых домов</td>
    </tr>
</table><br>

<strong>2. КОНСТРУКЦИЯ КРОВЕЛЬНОГО ПИРОГА</strong><br><br>

<strong>Для холодного чердака (снизу вверх):</strong><br>
1️⃣ Стропильная система<br>
2️⃣ Гидроизоляционная пленка (супердиффузионная мембрана)<br>
3️⃣ Контробрешетка 50×50 мм (вентзазор)<br>
4️⃣ Обрешетка (шаг зависит от покрытия)<br>
5️⃣ Кровельное покрытие<br><br>

<strong>Для утепленной мансарды:</strong><br>
1️⃣ Внутренняя отделка (гипсокартон)<br>
2️⃣ Пароизоляционная пленка<br>
3️⃣ Утеплитель между стропил (150-200 мм)<br>
4️⃣ Гидроветрозащитная мембрана<br>
5️⃣ Вентзазор 50 мм (контробрешетка)<br>
6️⃣ Обрешетка<br>
7️⃣ Кровельное покрытие<br><br>

<strong>💡 ПРАКТИЧЕСКИЕ ПРИМЕРЫ</strong><br><br>

<strong>Пример 1: Расчет площади кровли</strong><br>
<div style="background: #e8f5e9; padding: 15px; border-left: 4px solid #4caf50; margin: 10px 0;">
    <strong>Исходные данные:</strong><br>
    • Размеры дома: 10×12 м<br>
    • Двускатная кровля, угол 30°<br>
    • Свесы: 0.5 м с каждой стороны<br><br>

    <strong>Расчет:</strong><br>
    Длина ската = (12/2) / cos(30°) = 6.93 м<br>
    Ширина с учетом свесов = 10 + 2×0.5 = 11 м<br>
    Площадь одного ската = 6.93 × 11 = 76.2 м²<br>
    <strong>Общая площадь кровли = 76.2 × 2 = 152.4 м²</strong><br><br>

    С учетом отходов (+10%): <strong>167.6 м²</strong><br>
    Количество листов металлочерепицы (1.18×3.5 м): <strong>41 лист</strong>
</div><br>

<strong>Пример 2: Расчет вентиляционного зазора</strong><br>
<div style="background: #fff3e0; padding: 15px; border-left: 4px solid #ff9800; margin: 10px 0;">
    <strong>Минимальная высота вентзазора (СП 17.13330, п. 6.5):</strong><br>
    • Для металлочерепицы: <strong>50 мм</strong><br>
    • Для гибкой черепицы: <strong>50 мм</strong><br>
    • Для профнастила: <strong>60 мм</strong><br><br>

    <strong>Площадь вентотверстий:</strong><br>
    S_вент = 0.002 × S_кровли<br>
    Для кровли 150 м²: S_вент = 0.3 м² = <strong>3000 см²</strong><br>
    Распределяется: конек + карнизные продухи
</div><br>

<strong>📚 НОРМАТИВНЫЕ ДОКУМЕНТЫ</strong><br>
• <strong>СП 17.13330.2017</strong> "Кровли" (актуализированная редакция СНиП II-26-76)<br>
• <strong>СП 71.13330.2017</strong> "Изоляционные и отделочные покрытия"<br>
• <strong>ГОСТ 30547-97</strong> "Материалы рулонные кровельные и гидроизоляционные"<br>
• <strong>ГОСТ 24045-2016</strong> "Профили стальные листовые гнутые с трапециевидными гофрами"<br>
• <strong>СП 20.13330.2016</strong> "Нагрузки и воздействия" (снеговые нагрузки)
"""

    def _get_insulation_content(self) -> str:
        """Контент по теплоизоляции"""
        return """
<strong>📋 ВВЕДЕНИЕ</strong><br>
Теплоизоляция - комплекс мер по снижению теплопередачи между внутренним и наружным пространством. Правильное утепление снижает энергопотребление на 40-60%.<br><br>

<strong>🔍 ДЕТАЛЬНАЯ ИНФОРМАЦИЯ</strong><br><br>

<strong>1. ВИДЫ УТЕПЛИТЕЛЕЙ (СП 50.13330.2012)</strong><br><br>

<table style="width:100%; border-collapse: collapse; margin: 15px 0;">
    <tr style="background: #3498db; color: white;">
        <th style="padding: 10px; border: 1px solid #ddd;">Материал</th>
        <th style="padding: 10px; border: 1px solid #ddd;">λ, Вт/(м·°C)</th>
        <th style="padding: 10px; border: 1px solid #ddd;">Плотность</th>
        <th style="padding: 10px; border: 1px solid #ddd;">Горючесть</th>
        <th style="padding: 10px; border: 1px solid #ddd;">Применение</th>
    </tr>
    <tr>
        <td style="padding: 10px; border: 1px solid #ddd;"><strong>Минвата (каменная)</strong></td>
        <td style="padding: 10px; border: 1px solid #ddd;">0.035-0.045</td>
        <td style="padding: 10px; border: 1px solid #ddd;">30-200 кг/м³</td>
        <td style="padding: 10px; border: 1px solid #ddd;">НГ (негорючая)</td>
        <td style="padding: 10px; border: 1px solid #ddd;">Универсальное</td>
    </tr>
    <tr style="background: #f8f9fa;">
        <td style="padding: 10px; border: 1px solid #ddd;"><strong>Пенополистирол (ППС)</strong></td>
        <td style="padding: 10px; border: 1px solid #ddd;">0.036-0.041</td>
        <td style="padding: 10px; border: 1px solid #ddd;">15-35 кг/м³</td>
        <td style="padding: 10px; border: 1px solid #ddd;">Г1-Г4</td>
        <td style="padding: 10px; border: 1px solid #ddd;">Фундаменты, цоколь</td>
    </tr>
    <tr>
        <td style="padding: 10px; border: 1px solid #ddd;"><strong>ЭППС (экструдированный)</strong></td>
        <td style="padding: 10px; border: 1px solid #ddd;">0.028-0.034</td>
        <td style="padding: 10px; border: 1px solid #ddd;">28-45 кг/м³</td>
        <td style="padding: 10px; border: 1px solid #ddd;">Г1-Г4</td>
        <td style="padding: 10px; border: 1px solid #ddd;">Полы, отмостка</td>
    </tr>
    <tr style="background: #f8f9fa;">
        <td style="padding: 10px; border: 1px solid #ddd;"><strong>ППУ (напыляемый)</strong></td>
        <td style="padding: 10px; border: 1px solid #ddd;">0.023-0.035</td>
        <td style="padding: 10px; border: 1px solid #ddd;">30-80 кг/м³</td>
        <td style="padding: 10px; border: 1px solid #ddd;">Г2-Г3</td>
        <td style="padding: 10px; border: 1px solid #ddd;">Сложные формы</td>
    </tr>
    <tr>
        <td style="padding: 10px; border: 1px solid #ddd;"><strong>Эковата (целлюлоза)</strong></td>
        <td style="padding: 10px; border: 1px solid #ddd;">0.037-0.042</td>
        <td style="padding: 10px; border: 1px solid #ddd;">30-75 кг/м³</td>
        <td style="padding: 10px; border: 1px solid #ddd;">Г2</td>
        <td style="padding: 10px; border: 1px solid #ddd;">Каркасные дома</td>
    </tr>
</table><br>

<strong>2. ТРЕБУЕМОЕ СОПРОТИВЛЕНИЕ ТЕПЛОПЕРЕДАЧЕ (СП 50.13330, Приложение Е)</strong><br><br>

<strong>Для Москвы (ГСОП = 4943°С·сут):</strong><br>
• Стены: <strong>R_req = 3.13 м²·°C/Вт</strong><br>
• Перекрытие чердака: <strong>R_req = 4.70 м²·°C/Вт</strong><br>
• Перекрытие над подвалом: <strong>R_req = 3.36 м²·°C/Вт</strong><br>
• Окна: <strong>R_req = 0.54 м²·°C/Вт</strong><br><br>

<strong>Для Санкт-Петербурга (ГСОП = 5125):</strong><br>
• Стены: <strong>R_req = 3.23 м²·°C/Вт</strong><br>
• Чердак: <strong>R_req = 4.85 м²·°C/Вт</strong><br><br>

<strong>💡 ПРАКТИЧЕСКИЕ ПРИМЕРЫ</strong><br><br>

<strong>Пример 1: Расчет толщины утеплителя для стены</strong><br>
<div style="background: #e8f5e9; padding: 15px; border-left: 4px solid #4caf50; margin: 10px 0;">
    <strong>Исходные данные:</strong><br>
    • Москва (R_req = 3.13 м²·°C/Вт)<br>
    • Стена: кирпич 380 мм + минвата + облицовка<br>
    • λ_кирпича = 0.52 Вт/(м·°C)<br>
    • λ_минваты = 0.040 Вт/(м·°C)<br><br>

    <strong>Расчет:</strong><br>
    R_кирпича = 0.38 / 0.52 = 0.73 м²·°C/Вт<br>
    R_облицовки = 0.02 / 0.20 = 0.10 м²·°C/Вт<br>
    R_утеплителя = 3.13 - 0.73 - 0.10 = 2.30 м²·°C/Вт<br><br>

    δ_утеплителя = R × λ = 2.30 × 0.040 = 0.092 м = <strong>92 мм</strong><br>
    <strong>Принимаем: 100 мм минваты (2 слоя по 50 мм)</strong>
</div><br>

<strong>Пример 2: Расчет точки росы</strong><br>
<div style="background: #fff3e0; padding: 15px; border-left: 4px solid #ff9800; margin: 10px 0;">
    <strong>Условия:</strong><br>
    • Температура внутри: +22°C<br>
    • Влажность: 55%<br>
    • Температура снаружи: -20°C<br><br>

    <strong>Точка росы (упрощенная формула):</strong><br>
    T_р = (234.5 × α) / (17.27 - α)<br>
    где α = (17.27×T)/(237.3+T) + ln(RH/100)<br><br>

    <strong>Результат: T_р = +12.4°C</strong><br><br>

    <strong>Вывод:</strong> Точка росы находится внутри стены. Нужна паров диффузионная мембрана!
</div><br>

<strong>📚 НОРМАТИВНЫЕ ДОКУМЕНТЫ</strong><br>
• <strong>СП 50.13330.2012</strong> "Тепловая защита зданий"<br>
• <strong>СП 23-101-2004</strong> "Проектирование тепловой защиты зданий"<br>
• <strong>ГОСТ 30494-2011</strong> "Параметры микроклимата в помещениях"<br>
• <strong>ГОСТ 7076-99</strong> "Материалы и изделия строительные. Метод определения теплопроводности"
"""

    def _get_ventilation_content(self) -> str:
        """Контент по вентиляции"""
        return """
<strong>📋 ВВЕДЕНИЕ</strong><br>
Вентиляция - организованный воздухообмен, обеспечивающий удаление загрязненного воздуха и подачу свежего. Обязательна для поддержания здорового микроклимата.<br><br>

<strong>🔍 ДЕТАЛЬНАЯ ИНФОРМАЦИЯ</strong><br><br>

<strong>1. ТИПЫ ВЕНТИЛЯЦИОННЫХ СИСТЕМ (СП 60.13330.2020)</strong><br><br>

<table style="width:100%; border-collapse: collapse; margin: 15px 0;">
    <tr style="background: #3498db; color: white;">
        <th style="padding: 10px; border: 1px solid #ddd;">Тип системы</th>
        <th style="padding: 10px; border: 1px solid #ddd;">Принцип работы</th>
        <th style="padding: 10px; border: 1px solid #ddd;">КПД</th>
        <th style="padding: 10px; border: 1px solid #ddd;">Применение</th>
    </tr>
    <tr>
        <td style="padding: 10px; border: 1px solid #ddd;"><strong>Естественная</strong></td>
        <td style="padding: 10px; border: 1px solid #ddd;">Разница температур</td>
        <td style="padding: 10px; border: 1px solid #ddd;">-</td>
        <td style="padding: 10px; border: 1px solid #ddd;">Жилые дома до 5 этажей</td>
    </tr>
    <tr style="background: #f8f9fa;">
        <td style="padding: 10px; border: 1px solid #ddd;"><strong>Приточно-вытяжная</strong></td>
        <td style="padding: 10px; border: 1px solid #ddd;">Механическая</td>
        <td style="padding: 10px; border: 1px solid #ddd;">70-90%</td>
        <td style="padding: 10px; border: 1px solid #ddd;">Офисы, торговые центры</td>
    </tr>
    <tr>
        <td style="padding: 10px; border: 1px solid #ddd;"><strong>С рекуперацией</strong></td>
        <td style="padding: 10px; border: 1px solid #ddd;">Теплообменник</td>
        <td style="padding: 10px; border: 1px solid #ddd;">60-95%</td>
        <td style="padding: 10px; border: 1px solid #ddd;">Энергоэффективные дома</td>
    </tr>
    <tr style="background: #f8f9fa;">
        <td style="padding: 10px; border: 1px solid #ddd;"><strong>Децентрализованная</strong></td>
        <td style="padding: 10px; border: 1px solid #ddd;">Проветриватели</td>
        <td style="padding: 10px; border: 1px solid #ddd;">40-70%</td>
        <td style="padding: 10px; border: 1px solid #ddd;">Квартиры, небольшие дома</td>
    </tr>
</table><br>

<strong>2. НОРМЫ ВОЗДУХООБМЕНА (СП 60.13330, табл. 9.1)</strong><br><br>

<strong>Для жилых помещений:</strong><br>
• Жилая комната: <strong>30 м³/ч на человека</strong> или <strong>0.35 объема помещения/час</strong><br>
• Кухня с газовой плитой: <strong>90 м³/ч</strong><br>
• Кухня с электроплитой: <strong>60 м³/ч</strong><br>
• Ванная комната: <strong>25 м³/ч</strong><br>
• Туалет: <strong>25 м³/ч</strong><br>
• Совмещенный санузел: <strong>50 м³/ч</strong><br><br>

<strong>Для офисных помещений:</strong><br>
• Офис (на 1 человека): <strong>60 м³/ч</strong><br>
• Переговорная: <strong>40 м³/ч на человека</strong><br>
• Коридор: <strong>0.5 объема/час</strong><br><br>

<strong>💡 ПРАКТИЧЕСКИЕ ПРИМЕРЫ</strong><br><br>

<strong>Пример 1: Расчет производительности вентиляции для квартиры</strong><br>
<div style="background: #e8f5e9; padding: 15px; border-left: 4px solid #4caf50; margin: 10px 0;">
    <strong>Исходные данные:</strong><br>
    • 3-комнатная квартира<br>
    • Площадь: 75 м², высота потолков: 2.7 м<br>
    • Проживает 4 человека<br><br>

    <strong>Расчет по кратности:</strong><br>
    V = 75 × 2.7 = 202.5 м³<br>
    Q = 202.5 × 0.35 = <strong>71 м³/ч</strong><br><br>

    <strong>Расчет по людям:</strong><br>
    Q = 4 × 30 = <strong>120 м³/ч</strong><br><br>

    <strong>Плюс кухня: +60 м³/ч</strong><br>
    <strong>Плюс санузел: +25 м³/ч</strong><br><br>

    <strong>ИТОГО: минимум 205 м³/ч</strong><br>
    <strong>Рекомендуемый запас (+20%): 250 м³/ч</strong>
</div><br>

<strong>Пример 2: Выбор рекуператора</strong><br>
<div style="background: #fff3e0; padding: 15px; border-left: 4px solid #ff9800; margin: 10px 0;">
    <strong>Для квартиры 250 м³/ч:</strong><br><br>

    Экономия тепла в год (Москва):<br>
    E = Q × 0.33 × ΔT × t × КПД / 1000<br>
    E = 250 × 0.33 × 40 × 5800 × 0.80 / 1000 = <strong>15,312 кВт·ч/год</strong><br><br>

    При тарифе 5.5 руб/кВт·ч:<br>
    <strong>Экономия: 84,200 руб/год</strong><br><br>

    Стоимость установки: ~300,000 руб<br>
    <strong>Окупаемость: 3.6 года</strong>
</div><br>

<strong>📚 НОРМАТИВНЫЕ ДОКУМЕНТЫ</strong><br>
• <strong>СП 60.13330.2020</strong> "Отопление, вентиляция и кондиционирование воздуха"<br>
• <strong>ГОСТ 30494-2011</strong> "Здания жилые и общественные. Параметры микроклимата"<br>
• <strong>СНиП 41-01-2003</strong> "Отопление, вентиляция и кондиционирование"<br>
• <strong>ГОСТ 12.1.005-88</strong> "Общие санитарно-гигиенические требования к воздуху рабочей зоны"
"""

    def get_answer(self, question: str) -> Dict[str, Any]:
        """
        Получить структурированный ответ на вопрос

        Args:
            question: Вопрос пользователя

        Returns:
            Словарь с ответом и метаданными
        """
        question_lower = question.lower()

        # Поиск в базе знаний
        for topic_key, knowledge_item in self.knowledge_base.items():
            if any(keyword in question_lower for keyword in knowledge_item.keywords):
                logger.info(f"Found answer for topic: {topic_key}")

                return {
                    "answer": knowledge_item.content,
                    "metadata": {
                        "topic": knowledge_item.topic,
                        "complexity": knowledge_item.complexity.value,
                        "reading_time_minutes": knowledge_item.reading_time_minutes,
                        "key_terms": knowledge_item.key_terms,
                        "related_topics": knowledge_item.related_topics,
                        "regulations": knowledge_item.regulations
                    }
                }

        # Если точное совпадение не найдено
        return self._get_general_response()

    def _get_general_response(self) -> Dict[str, Any]:
        """Общий ответ со списком доступных тем"""
        content = """
<strong>AI КОНСУЛЬТАНТ ПО СТРОИТЕЛЬНЫМ НОРМАМ V2</strong><br><br>

<div style="background: #e8f4f8; padding: 20px; border-radius: 10px; margin: 15px 0;">
    <h3 style="color: #2c3e50;">📚 НОВЫЕ РАЗДЕЛЫ В БАЗЕ ЗНАНИЙ:</h3>

    <div style="margin: 15px 0;">
        <strong>🏠 КРОВЛЯ И КРОВЕЛЬНЫЕ РАБОТЫ</strong><br>
        • Типы кровельных покрытий<br>
        • Конструкция кровельного пирога<br>
        • Расчет площади и материалов<br>
        • Вентиляция подкровельного пространства<br>
        <em>Сложность: Средний | Время чтения: 12 мин</em>
    </div>

    <div style="margin: 15px 0;">
        <strong>🌡️ ТЕПЛОИЗОЛЯЦИЯ ЗДАНИЙ</strong><br>
        • Виды утеплителей и их характеристики<br>
        • Расчет толщины утеплителя<br>
        • Расчет точки росы<br>
        • Энергоэффективность<br>
        <em>Сложность: Средний | Время чтения: 10 мин</em>
    </div>

    <div style="margin: 15px 0;">
        <strong>💨 ВЕНТИЛЯЦИЯ И КОНДИЦИОНИРОВАНИЕ</strong><br>
        • Типы вентиляционных систем<br>
        • Нормы воздухообмена<br>
        • Расчет производительности<br>
        • Рекуперация тепла<br>
        <em>Сложность: Продвинутый | Время чтения: 15 мин</em>
    </div>
</div>

<strong>🔍 ПОПРОБУЙТЕ СПРОСИТЬ:</strong><br>
• "Какую кровлю выбрать для дома?"<br>
• "Как рассчитать толщину утеплителя для Москвы?"<br>
• "Какая вентиляция нужна для квартиры 75 м²?"<br><br>

<strong>Задайте конкретный вопрос по новым темам!</strong>
"""

        return {
            "answer": content,
            "metadata": {
                "topic": "Общая информация",
                "complexity": "Начальный",
                "reading_time_minutes": 2,
                "key_terms": ["кровля", "теплоизоляция", "вентиляция"],
                "related_topics": [],
                "regulations": []
            }
        }


# Singleton instance
ai_consultant_service_v2 = AIConsultantServiceV2()
