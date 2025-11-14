"""
Скрипт для инициализации тестовых данных
"""
import sys
import os

# Добавляем путь к приложению
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app.database import SessionLocal
from app.models.user import User, UserRole
from app.models.project import Project, ProjectType, ProjectStatus
from app.models.regulation import Regulation
from app.api.v1.endpoints.auth import get_password_hash
from datetime import datetime, timedelta

def init_users(db):
    """Создание тестовых пользователей"""
    users = [
        {
            "email": "admin@tehnadzor.ru",
            "full_name": "Администратор Системы",
            "position": "Системный администратор",
            "company": "ТехНадзор",
            "role": UserRole.ADMIN,
            "password": "Admin123!"
        },
        {
            "email": "engineer@tehnadzor.ru",
            "full_name": "Иван Петров",
            "position": "Старший инженер",
            "company": "СтройКонтроль",
            "role": UserRole.ENGINEER,
            "password": "Engineer123!"
        },
        {
            "email": "supervisor@tehnadzor.ru",
            "full_name": "Мария Сидорова",
            "position": "Руководитель отдела",
            "company": "СтройКонтроль",
            "role": UserRole.SUPERVISOR,
            "password": "Supervisor123!"
        }
    ]

    created_users = []
    for user_data in users:
        # Проверяем существование
        existing = db.query(User).filter(User.email == user_data["email"]).first()
        if existing:
            print(f"Пользователь {user_data['email']} уже существует")
            created_users.append(existing)
            continue

        password = user_data.pop("password")
        user = User(
            **user_data,
            hashed_password=get_password_hash(password),
            is_active=True,
            is_verified=True
        )
        db.add(user)
        created_users.append(user)
        print(f"Создан пользователь: {user.email}")

    db.commit()
    return created_users


def init_projects(db, users):
    """Создание тестовых проектов"""
    projects = [
        {
            "name": "ЖК 'Новый горизонт'",
            "description": "Жилой комплекс на 500 квартир, монолитное строительство",
            "project_type": ProjectType.RESIDENTIAL,
            "status": ProjectStatus.IN_PROGRESS,
            "address": "г. Москва, Ленинский проспект, д. 123",
            "city": "Москва",
            "region": "Московская область",
            "latitude": 55.751244,
            "longitude": 37.618423,
            "completion_percentage": 68.0,
            "start_date": datetime.now() - timedelta(days=180),
            "planned_end_date": datetime.now() + timedelta(days=365)
        },
        {
            "name": "Торговый центр 'Галерея'",
            "description": "Торгово-развлекательный центр, 3 этажа",
            "project_type": ProjectType.COMMERCIAL,
            "status": ProjectStatus.IN_PROGRESS,
            "address": "г. Санкт-Петербург, пр. Невский, д. 50",
            "city": "Санкт-Петербург",
            "region": "Ленинградская область",
            "latitude": 59.934280,
            "longitude": 30.335099,
            "completion_percentage": 45.0,
            "start_date": datetime.now() - timedelta(days=90),
            "planned_end_date": datetime.now() + timedelta(days=270)
        },
        {
            "name": "Производственный комплекс 'Завод №1'",
            "description": "Промышленный объект с цехами и складами",
            "project_type": ProjectType.INDUSTRIAL,
            "status": ProjectStatus.PLANNING,
            "address": "г. Казань, ул. Производственная, д. 10",
            "city": "Казань",
            "region": "Республика Татарстан",
            "completion_percentage": 0.0,
            "planned_end_date": datetime.now() + timedelta(days=500)
        }
    ]

    created_projects = []
    for project_data in projects:
        project = Project(**project_data, created_by=users[1].id)
        db.add(project)
        created_projects.append(project)
        print(f"Создан проект: {project.name}")

    db.commit()
    return created_projects


def init_regulations(db):
    """Создание базовых нормативов"""
    regulations = [
        {
            "code": "СП 63.13330.2018",
            "title": "Бетонные и железобетонные конструкции. Основные положения",
            "regulation_type": "СП",
            "description": "Свод правил по проектированию и строительству бетонных и железобетонных конструкций",
            "is_active": True
        },
        {
            "code": "СП 70.13330.2012",
            "title": "Несущие и ограждающие конструкции",
            "regulation_type": "СП",
            "description": "Актуализированная редакция СНиП 3.03.01-87",
            "is_active": True
        },
        {
            "code": "ГОСТ 7473-2010",
            "title": "Смеси бетонные. Технические условия",
            "regulation_type": "ГОСТ",
            "description": "Технические условия на бетонные смеси",
            "is_active": True
        },
        {
            "code": "СП 28.13330.2017",
            "title": "Защита строительных конструкций от коррозии",
            "regulation_type": "СП",
            "description": "Актуализированная редакция СНиП 2.03.11-85",
            "is_active": True
        },
        {
            "code": "СП 71.13330.2017",
            "title": "Изоляционные и отделочные покрытия",
            "regulation_type": "СП",
            "description": "Актуализированная редакция СНиП 3.04.01-87",
            "is_active": True
        }
    ]

    created_regulations = []
    for reg_data in regulations:
        # Проверяем существование
        existing = db.query(Regulation).filter(Regulation.code == reg_data["code"]).first()
        if existing:
            print(f"Норматив {reg_data['code']} уже существует")
            continue

        regulation = Regulation(**reg_data)
        db.add(regulation)
        created_regulations.append(regulation)
        print(f"Создан норматив: {regulation.code}")

    db.commit()
    return created_regulations


def main():
    """Главная функция инициализации"""
    print("=== Инициализация тестовых данных ===\n")

    db = SessionLocal()

    try:
        # Создание пользователей
        print("Создание пользователей...")
        users = init_users(db)

        # Создание проектов
        print("\nСоздание проектов...")
        projects = init_projects(db, users)

        # Создание нормативов
        print("\nСоздание нормативов...")
        regulations = init_regulations(db)

        print("\n=== Инициализация завершена успешно! ===")
        print(f"\nСоздано:")
        print(f"  - Пользователей: {len(users)}")
        print(f"  - Проектов: {len(projects)}")
        print(f"  - Нормативов: {len(regulations)}")

        print("\nТестовые учетные записи:")
        print("  admin@tehnadzor.ru / Admin123!")
        print("  engineer@tehnadzor.ru / Engineer123!")
        print("  supervisor@tehnadzor.ru / Supervisor123!")

    except Exception as e:
        print(f"\nОшибка при инициализации: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
