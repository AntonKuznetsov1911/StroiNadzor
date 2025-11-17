"""
Скрипт для заполнения базы данных реалистичными тестовыми данными
"""
import asyncio
import sys
from pathlib import Path
from datetime import datetime, date, timedelta
from decimal import Decimal
import random

# Добавляем путь к приложению
sys.path.append(str(Path(__file__).parent))

from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import async_session_maker, engine, Base
from app.models import (
    User, Project, Inspection, InspectionPhoto, DefectDetection,
    HiddenWork, HiddenWorkAct, ChecklistTemplate, Checklist, ChecklistItem,
    Document, Material, MaterialCertificate, Regulation
)
from app.core.security import get_password_hash


# Реалистичные данные для российского строительства
RUSSIAN_CITIES = [
    "Москва", "Санкт-Петербург", "Казань", "Новосибирск", "Екатеринбург",
    "Нижний Новгород", "Самара", "Омск", "Челябинск", "Ростов-на-Дону"
]

CONSTRUCTION_COMPANIES = [
    "ООО 'СтройГарант'", "ПАО 'МосСтрой'", "ЗАО 'ТехноСтрой'",
    "ООО 'СтройИнвест'", "АО 'СпецСтройМонтаж'", "ООО 'МегаСтрой'",
    "ПАО 'СтройКомплекс'", "ООО 'РосСтройПроект'"
]

STREET_NAMES = [
    "ул. Ленина", "Пр. Мира", "ул. Гагарина", "ул. Советская", "ул. Строителей",
    "Пр. Победы", "ул. Центральная", "ул. Кирова", "Пр. Комсомольский", "ул. Садовая"
]

PROJECT_TYPES = [
    "Жилой многоквартирный дом", "Торговый центр", "Офисное здание",
    "Производственный корпус", "Школа", "Детский сад", "Больница",
    "Спортивный комплекс", "Парковка многоуровневая"
]

MATERIAL_CATEGORIES = {
    "Бетон и раствор": ["Бетон B25", "Бетон B30", "Цементно-песчаный раствор М150"],
    "Арматура": ["Арматура A500C d12", "Арматура A500C d16", "Арматура A240 d8"],
    "Кирпич": ["Кирпич керамический рядовой", "Кирпич облицовочный", "Кирпич силикатный"],
    "Утеплитель": ["Минеральная вата 100мм", "Пенополистирол 50мм", "Базальтовая вата"],
    "Гидроизоляция": ["Гидроизол ГИ-Г", "Техноэласт ЭПП", "Бикрост ХПП"],
    "Кровля": ["Металлочерепица", "Профнастил С21", "Гибкая черепица"],
    "Окна": ["Стеклопакет 2-камерный", "Окно ПВХ 1500x1400", "Фурнитура оконная"],
}

SUPPLIERS = [
    "ООО 'СтройМатериалы'", "ТД 'Строй-Опт'", "Компания 'БетонСнаб'",
    "ООО 'АрматураПлюс'", "Завод 'ЖБИ-1'", "ТД 'КровляСервис'"
]

REGULATIONS_DATA = [
    {
        "code": "СП 63.13330.2018",
        "title": "Бетонные и железобетонные конструкции. Основные положения",
        "type": "sp",
        "category": "construction",
        "description": "Свод правил устанавливает требования к проектированию, изготовлению и контролю качества бетонных и железобетонных конструкций зданий и сооружений различного назначения.",
    },
    {
        "code": "СП 22.13330.2016",
        "title": "Основания зданий и сооружений",
        "type": "sp",
        "category": "construction",
        "description": "Свод правил распространяется на проектирование оснований зданий и сооружений различного назначения.",
    },
    {
        "code": "СП 50.13330.2012",
        "title": "Тепловая защита зданий",
        "type": "sp",
        "category": "technical",
        "description": "Свод правил устанавливает требования к тепловой защите зданий с целью экономии энергии при их эксплуатации.",
    },
    {
        "code": "СП 17.13330.2017",
        "title": "Кровли",
        "type": "sp",
        "category": "construction",
        "description": "Свод правил распространяется на проектирование и устройство кровель зданий и сооружений.",
    },
    {
        "code": "ГОСТ 8829-94",
        "title": "Изделия строительные железобетонные и бетонные заводского изготовления",
        "type": "gost",
        "category": "technical",
        "description": "Стандарт устанавливает общие технические требования к сборным железобетонным и бетонным изделиям.",
    },
    {
        "code": "ГОСТ 10884-94",
        "title": "Сталь арматурная термомеханически упрочненная для железобетонных конструкций",
        "type": "gost",
        "category": "technical",
        "description": "Стандарт распространяется на горячекатаную арматурную сталь периодического профиля.",
    },
    {
        "code": "СП 2.13130.2020",
        "title": "Системы противопожарной защиты. Обеспечение огнестойкости объектов защиты",
        "type": "sp",
        "category": "fire_safety",
        "description": "Свод правил устанавливает требования пожарной безопасности к огнестойкости зданий и сооружений.",
    },
    {
        "code": "СанПиН 2.1.3684-21",
        "title": "Санитарно-эпидемиологические требования к содержанию территорий городских и сельских поселений",
        "type": "sanpin",
        "category": "sanitary",
        "description": "Санитарные правила и нормы устанавливают обязательные санитарно-эпидемиологические требования.",
    },
]

CHECKLIST_TEMPLATES = [
    {
        "name": "Приемка фундамента",
        "category": "Фундаментные работы",
        "description": "Проверка качества выполнения фундаментных работ",
        "items": [
            {"title": "Проверка геометрических размеров", "order": 1, "priority": "high"},
            {"title": "Контроль качества бетона (прочность)", "order": 2, "priority": "critical"},
            {"title": "Проверка армирования", "order": 3, "priority": "high"},
            {"title": "Контроль гидроизоляции", "order": 4, "priority": "high"},
            {"title": "Проверка осадки фундамента", "order": 5, "priority": "medium"},
        ]
    },
    {
        "name": "Приемка кирпичной кладки",
        "category": "Каменные работы",
        "description": "Контроль качества кирпичной кладки",
        "items": [
            {"title": "Проверка вертикальности стен", "order": 1, "priority": "high"},
            {"title": "Контроль толщины швов", "order": 2, "priority": "medium"},
            {"title": "Проверка перевязки швов", "order": 3, "priority": "high"},
            {"title": "Контроль качества раствора", "order": 4, "priority": "high"},
            {"title": "Проверка проёмов", "order": 5, "priority": "medium"},
        ]
    },
    {
        "name": "Приемка кровли",
        "category": "Кровельные работы",
        "description": "Контроль качества кровельных работ",
        "items": [
            {"title": "Проверка уклонов кровли", "order": 1, "priority": "high"},
            {"title": "Контроль качества покрытия", "order": 2, "priority": "critical"},
            {"title": "Проверка гидроизоляции", "order": 3, "priority": "critical"},
            {"title": "Контроль водосточной системы", "order": 4, "priority": "medium"},
            {"title": "Проверка примыканий и узлов", "order": 5, "priority": "high"},
        ]
    },
]


async def create_users(session: AsyncSession) -> list[User]:
    """Создание тестовых пользователей"""
    users_data = [
        {
            "username": "admin",
            "email": "admin@stroinadzor.ru",
            "full_name": "Администратор Системы",
            "role": "admin",
            "is_active": True,
        },
        {
            "username": "engineer1",
            "email": "ivanov@stroinadzor.ru",
            "full_name": "Иванов Иван Петрович",
            "role": "engineer",
            "is_active": True,
        },
        {
            "username": "engineer2",
            "email": "petrova@stroinadzor.ru",
            "full_name": "Петрова Мария Сергеевна",
            "role": "engineer",
            "is_active": True,
        },
        {
            "username": "supervisor",
            "email": "sidorov@stroinadzor.ru",
            "full_name": "Сидоров Петр Михайлович",
            "role": "supervisor",
            "is_active": True,
        },
        {
            "username": "inspector",
            "email": "kozlov@stroinadzor.ru",
            "full_name": "Козлов Сергей Александрович",
            "role": "inspector",
            "is_active": True,
        },
    ]

    users = []
    for user_data in users_data:
        user = User(
            **user_data,
            hashed_password=get_password_hash("password123"),
            phone=f"+7-{random.randint(900, 999)}-{random.randint(100, 999)}-{random.randint(10, 99)}-{random.randint(10, 99)}",
            position=f"Инженер {random.choice(['I', 'II', 'III'])} категории" if user_data["role"] == "engineer" else "Руководитель отдела"
        )
        session.add(user)
        users.append(user)

    await session.flush()
    print(f"✓ Создано {len(users)} пользователей")
    return users


async def create_projects(session: AsyncSession, users: list[User]) -> list[Project]:
    """Создание тестовых проектов"""
    projects = []

    for i in range(8):
        city = random.choice(RUSSIAN_CITIES)
        street = random.choice(STREET_NAMES)
        project_type = random.choice(PROJECT_TYPES)

        start_date = date.today() - timedelta(days=random.randint(90, 365))
        end_date = start_date + timedelta(days=random.randint(180, 730))

        status = random.choice(["planning", "in_progress", "in_progress", "completed"])
        if date.today() < start_date:
            status = "planning"
        elif date.today() > end_date:
            status = "completed"

        project = Project(
            name=f"{project_type} по адресу: г. {city}, {street}, д. {random.randint(1, 150)}",
            description=f"Строительство {project_type.lower()} общей площадью {random.randint(1000, 15000)} кв.м",
            address=f"{random.randint(100000, 999999)}, г. {city}, {street}, д. {random.randint(1, 150)}",
            customer=random.choice(CONSTRUCTION_COMPANIES),
            contractor=random.choice(CONSTRUCTION_COMPANIES),
            start_date=start_date,
            end_date=end_date,
            status=status,
            budget=Decimal(random.randint(50000000, 500000000)),
            created_by_id=random.choice(users).id,
        )
        session.add(project)
        projects.append(project)

    await session.flush()
    print(f"✓ Создано {len(projects)} проектов")
    return projects


async def create_regulations(session: AsyncSession) -> list[Regulation]:
    """Создание нормативных документов"""
    regulations = []

    for reg_data in REGULATIONS_DATA:
        regulation = Regulation(
            code=reg_data["code"],
            title=reg_data["title"],
            regulation_type=reg_data["type"],
            category=reg_data["category"],
            description=reg_data["description"],
            effective_date=date(2020, 1, 1),
            is_active=True,
            keywords=["строительство", "нормы", "требования"],
            related_regulations=[],
            view_count=random.randint(10, 500),
            reference_count=random.randint(5, 100),
        )
        session.add(regulation)
        regulations.append(regulation)

    await session.flush()
    print(f"✓ Создано {len(regulations)} нормативных документов")
    return regulations


async def create_checklist_templates(session: AsyncSession, users: list[User]) -> list[ChecklistTemplate]:
    """Создание шаблонов чек-листов"""
    templates = []

    for template_data in CHECKLIST_TEMPLATES:
        template = ChecklistTemplate(
            name=template_data["name"],
            category=template_data["category"],
            description=template_data["description"],
            is_active=True,
            created_by_id=random.choice(users).id,
        )
        session.add(template)
        await session.flush()

        # Добавляем пункты
        for item_data in template_data["items"]:
            from app.models.checklist import ChecklistTemplateItem
            item = ChecklistTemplateItem(
                template_id=template.id,
                title=item_data["title"],
                order=item_data["order"],
                priority=item_data["priority"],
                is_mandatory=True,
            )
            session.add(item)

        templates.append(template)

    await session.flush()
    print(f"✓ Создано {len(templates)} шаблонов чек-листов")
    return templates


async def create_materials(session: AsyncSession, projects: list[Project]) -> list[Material]:
    """Создание материалов"""
    materials = []

    for project in projects[:6]:  # Для 6 проектов
        for category, materials_list in MATERIAL_CATEGORIES.items():
            for material_name in materials_list[:2]:  # По 2 материала из каждой категории
                quantity = Decimal(random.randint(10, 1000))
                unit_price = Decimal(random.randint(100, 10000))

                material = Material(
                    project_id=project.id,
                    name=material_name,
                    category=category,
                    manufacturer=f"ОАО '{random.choice(['Стройматериалы', 'Бетон', 'АрматураПром', 'ЖБИ'])}'",
                    specification=f"ГОСТ {random.randint(1000, 30000)}-{random.randint(80, 2020)}",
                    quantity=quantity,
                    unit="м3" if "Бетон" in material_name else "т" if "Арматура" in material_name else "шт",
                    unit_price=unit_price,
                    total_price=quantity * unit_price,
                    supplier=random.choice(SUPPLIERS),
                    delivery_date=date.today() + timedelta(days=random.randint(-30, 60)),
                    notes=f"Материал для {project.name[:50]}",
                )
                session.add(material)
                materials.append(material)

    await session.flush()
    print(f"✓ Создано {len(materials)} материалов")
    return materials


async def create_material_certificates(session: AsyncSession, materials: list[Material], users: list[User]) -> list[MaterialCertificate]:
    """Создание сертификатов материалов"""
    certificates = []

    for material in materials[:30]:  # Для 30 материалов
        cert = MaterialCertificate(
            material_id=material.id,
            certificate_number=f"СС-{random.randint(1000, 9999)}-{random.randint(20, 24)}",
            certificate_type=random.choice(["Сертификат соответствия", "Декларация соответствия", "Паспорт качества"]),
            issuing_authority=random.choice([
                "Росстандарт",
                "Ростехнадзор",
                "Федеральное агентство по техническому регулированию",
                "ФБУ 'Тест-С.-Петербург'"
            ]),
            issue_date=date.today() - timedelta(days=random.randint(30, 365)),
            expiry_date=date.today() + timedelta(days=random.randint(30, 1095)),
            is_valid=True,
            uploaded_by_id=random.choice(users).id,
            notes="Оригинал сертификата в архиве отдела",
        )
        session.add(cert)
        certificates.append(cert)

    await session.flush()
    print(f"✓ Создано {len(certificates)} сертификатов")
    return certificates


async def create_inspections(session: AsyncSession, projects: list[Project], users: list[User]) -> list[Inspection]:
    """Создание осмотров"""
    inspections = []

    inspection_types = [
        "Входной контроль материалов",
        "Операционный контроль",
        "Приёмочный контроль",
        "Контроль скрытых работ"
    ]

    for project in projects[:6]:
        for _ in range(random.randint(3, 8)):
            inspection_date = project.start_date + timedelta(days=random.randint(0, 180))

            inspection = Inspection(
                project_id=project.id,
                inspection_type=random.choice(inspection_types),
                inspection_date=inspection_date,
                inspector_id=random.choice([u.id for u in users if u.role in ["engineer", "inspector"]]),
                location=f"Объект: {project.address}",
                weather_conditions=random.choice(["Ясно, +20°C", "Облачно, +15°C", "Дождь, +10°C", "Солнечно, +25°C"]),
                findings=f"Обнаружено {random.randint(0, 5)} замечаний",
                recommendations="Устранить выявленные замечания в течение 5 рабочих дней",
                status=random.choice(["completed", "completed", "pending"]),
                defects_count=random.randint(0, 3),
            )
            session.add(inspection)
            inspections.append(inspection)

    await session.flush()
    print(f"✓ Создано {len(inspections)} осмотров")
    return inspections


async def create_hidden_works(session: AsyncSession, projects: list[Project], users: list[User]) -> list[HiddenWork]:
    """Создание скрытых работ"""
    hidden_works = []

    work_types = ["foundation", "reinforcement", "welding", "waterproofing", "electrical", "plumbing"]

    for project in projects[:5]:
        for work_type in work_types[:random.randint(3, 5)]:
            work = HiddenWork(
                project_id=project.id,
                work_type=work_type,
                description=f"Скрытые работы: {work_type}",
                location=f"Секция {random.randint(1, 5)}, этаж {random.randint(1, 10)}",
                responsible_contractor=project.contractor,
                responsible_person="Прораб " + random.choice(["Иванов И.И.", "Петров П.П.", "Сидоров С.С."]),
                planned_date=project.start_date + timedelta(days=random.randint(30, 120)),
                status=random.choice(["pending", "in_progress", "completed", "approved"]),
                notes="Требуется освидетельствование",
                created_by_id=random.choice(users).id,
            )
            session.add(work)
            hidden_works.append(work)

    await session.flush()
    print(f"✓ Создано {len(hidden_works)} скрытых работ")
    return hidden_works


async def create_documents(session: AsyncSession, projects: list[Project], users: list[User]) -> list[Document]:
    """Создание документов"""
    documents = []

    doc_types = ["permit", "act", "protocol", "certificate", "technical", "financial"]

    for project in projects[:6]:
        for _ in range(random.randint(5, 12)):
            doc_type = random.choice(doc_types)
            doc = Document(
                project_id=project.id,
                title=f"{doc_type.upper()}-{random.randint(1000, 9999)} для {project.name[:30]}",
                document_type=doc_type,
                description=f"Документ типа {doc_type}",
                file_path=f"/storage/documents/{project.id}/{doc_type}_{random.randint(1000, 9999)}.pdf",
                file_size=random.randint(100000, 5000000),
                mime_type="application/pdf",
                version=1,
                status="approved" if random.random() > 0.3 else "pending",
                uploaded_by_id=random.choice(users).id,
                notes="Оригинал в архиве",
            )
            session.add(doc)
            documents.append(doc)

    await session.flush()
    print(f"✓ Создано {len(documents)} документов")
    return documents


async def create_checklists(session: AsyncSession, projects: list[Project], templates: list[ChecklistTemplate], users: list[User]) -> list[Checklist]:
    """Создание чек-листов"""
    checklists = []

    for project in projects[:5]:
        for template in templates:
            checklist = Checklist(
                project_id=project.id,
                name=f"{template.name} - {project.name[:40]}",
                description=template.description,
                status=random.choice(["not_started", "in_progress", "completed"]),
                created_by_id=random.choice(users).id,
            )
            session.add(checklist)
            await session.flush()

            # Создаём пункты из шаблона
            from app.models.checklist import ChecklistTemplateItem
            template_items = await session.execute(
                session.query(ChecklistTemplateItem).filter_by(template_id=template.id)
            )

            checklists.append(checklist)

    await session.flush()
    print(f"✓ Создано {len(checklists)} чек-листов")
    return checklists


async def main():
    """Основная функция"""
    print("=" * 60)
    print("Заполнение базы данных тестовыми данными")
    print("=" * 60)

    # Создаём таблицы
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    print("✓ Таблицы созданы\n")

    # Заполняем данными
    async with async_session_maker() as session:
        try:
            print("Создание данных...\n")

            users = await create_users(session)
            projects = await create_projects(session, users)
            regulations = await create_regulations(session)
            templates = await create_checklist_templates(session, users)
            materials = await create_materials(session, projects)
            certificates = await create_material_certificates(session, materials, users)
            inspections = await create_inspections(session, projects, users)
            hidden_works = await create_hidden_works(session, projects, users)
            documents = await create_documents(session, projects, users)
            checklists = await create_checklists(session, projects, templates, users)

            await session.commit()

            print("\n" + "=" * 60)
            print("✅ База данных успешно заполнена!")
            print("=" * 60)
            print(f"\nСоздано:")
            print(f"  • Пользователей: {len(users)}")
            print(f"  • Проектов: {len(projects)}")
            print(f"  • Нормативов: {len(regulations)}")
            print(f"  • Шаблонов чек-листов: {len(templates)}")
            print(f"  • Материалов: {len(materials)}")
            print(f"  • Сертификатов: {len(certificates)}")
            print(f"  • Осмотров: {len(inspections)}")
            print(f"  • Скрытых работ: {len(hidden_works)}")
            print(f"  • Документов: {len(documents)}")
            print(f"  • Чек-листов: {len(checklists)}")
            print("\nТестовые учётные данные:")
            print("  • Администратор: admin / password123")
            print("  • Инженер: engineer1 / password123")
            print("  • Супервайзер: supervisor / password123")

        except Exception as e:
            await session.rollback()
            print(f"\n❌ Ошибка при заполнении БД: {e}")
            raise


if __name__ == "__main__":
    asyncio.run(main())
