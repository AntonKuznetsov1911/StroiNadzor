"""
Скрипт для заполнения БД тестовыми данными
"""
import sys
import os
from datetime import datetime, timedelta
from pathlib import Path

# Добавляем путь к приложению
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models import (
    User, Project, Inspection, InspectionPhoto,
    DefectDetection, HiddenWork, Document, Regulation
)
from app.security import get_password_hash


def create_test_users(db: Session):
    """Создание тестовых пользователей"""
    print("Создание тестовых пользователей...")

    users_data = [
        {
            "email": "admin@tehnadzor.ru",
            "full_name": "Администратор",
            "role": "admin",
            "password": "admin123"
        },
        {
            "email": "supervisor@tehnadzor.ru",
            "full_name": "Супервайзер Иванов",
            "role": "supervisor",
            "password": "super123"
        },
        {
            "email": "inspector@tehnadzor.ru",
            "full_name": "Инспектор Петров",
            "role": "inspector",
            "password": "inspect123"
        },
        {
            "email": "engineer@tehnadzor.ru",
            "full_name": "Инженер Сидоров",
            "role": "engineer",
            "password": "eng123"
        },
        {
            "email": "client@tehnadzor.ru",
            "full_name": "Клиент Смирнов",
            "role": "client",
            "password": "client123"
        },
    ]

    users = []
    for user_data in users_data:
        # Проверяем, существует ли пользователь
        existing_user = db.query(User).filter(User.email == user_data["email"]).first()
        if existing_user:
            print(f"  Пользователь {user_data['email']} уже существует, пропускаем")
            users.append(existing_user)
            continue

        user = User(
            email=user_data["email"],
            full_name=user_data["full_name"],
            role=user_data["role"],
            hashed_password=get_password_hash(user_data["password"]),
            is_active=True
        )
        db.add(user)
        users.append(user)
        print(f"  Создан пользователь: {user_data['email']} (пароль: {user_data['password']})")

    db.commit()
    print(f"Создано пользователей: {len(users)}")
    return users


def create_test_projects(db: Session, users: list):
    """Создание тестовых проектов"""
    print("\nСоздание тестовых проектов...")

    admin = next((u for u in users if u.role == "admin"), users[0])

    projects_data = [
        {
            "name": "ЖК 'Северный'",
            "address": "г. Москва, ул. Северная, д. 1",
            "description": "Строительство жилого комплекса",
            "status": "in_progress",
            "start_date": datetime.now() - timedelta(days=60),
            "planned_end_date": datetime.now() + timedelta(days=120),
            "latitude": 55.7558,
            "longitude": 37.6173
        },
        {
            "name": "БЦ 'Технопарк'",
            "address": "г. Москва, ул. Ленина, д. 50",
            "description": "Строительство бизнес-центра",
            "status": "planning",
            "start_date": datetime.now() + timedelta(days=30),
            "planned_end_date": datetime.now() + timedelta(days=365),
            "latitude": 55.7500,
            "longitude": 37.6200
        },
        {
            "name": "Торговый центр 'Метрополис'",
            "address": "г. Москва, просп. Мира, д. 100",
            "description": "Реконструкция торгового центра",
            "status": "completed",
            "start_date": datetime.now() - timedelta(days=180),
            "planned_end_date": datetime.now() - timedelta(days=10),
            "end_date": datetime.now() - timedelta(days=5),
            "latitude": 55.7700,
            "longitude": 37.6400
        },
        {
            "name": "Школа №123",
            "address": "г. Москва, ул. Школьная, д. 5",
            "description": "Капитальный ремонт школы",
            "status": "in_progress",
            "start_date": datetime.now() - timedelta(days=45),
            "planned_end_date": datetime.now() + timedelta(days=90),
            "latitude": 55.7400,
            "longitude": 37.6100
        },
        {
            "name": "Парковка 'Центральная'",
            "address": "г. Москва, ул. Центральная, д. 25",
            "description": "Строительство многоуровневой парковки",
            "status": "suspended",
            "start_date": datetime.now() - timedelta(days=90),
            "planned_end_date": datetime.now() + timedelta(days=60),
            "latitude": 55.7600,
            "longitude": 37.6300
        },
    ]

    projects = []
    for proj_data in projects_data:
        project = Project(
            **proj_data,
            created_by_id=admin.id
        )
        db.add(project)
        projects.append(project)
        print(f"  Создан проект: {proj_data['name']}")

    db.commit()
    print(f"Создано проектов: {len(projects)}")
    return projects


def create_test_inspections(db: Session, projects: list, users: list):
    """Создание тестовых проверок"""
    print("\nСоздание тестовых проверок...")

    inspector = next((u for u in users if u.role == "inspector"), users[0])

    inspections = []
    for project in projects:
        if project.status in ["in_progress", "completed"]:
            # Создаем 2-3 проверки на проект
            num_inspections = 3 if project.status == "completed" else 2

            for i in range(num_inspections):
                inspection = Inspection(
                    project_id=project.id,
                    inspection_type="scheduled" if i == 0 else "unscheduled",
                    result="compliant" if i % 2 == 0 else "non_compliant",
                    description=f"Проверка #{i+1} проекта {project.name}",
                    location_description=f"Участок {i+1}",
                    inspector_notes=f"Замечания к проверке #{i+1}",
                    inspector_id=inspector.id,
                    latitude=project.latitude + (i * 0.001),
                    longitude=project.longitude + (i * 0.001),
                    created_at=datetime.now() - timedelta(days=(num_inspections - i) * 10)
                )
                db.add(inspection)
                inspections.append(inspection)

    db.commit()
    print(f"Создано проверок: {len(inspections)}")
    return inspections


def create_test_hidden_works(db: Session, projects: list, users: list):
    """Создание тестовых скрытых работ"""
    print("\nСоздание тестовых скрытых работ...")

    engineer = next((u for u in users if u.role == "engineer"), users[0])
    inspector = next((u for u in users if u.role == "inspector"), users[0])

    hidden_works = []
    for project in projects:
        if project.status == "in_progress":
            # Создаем 1-2 скрытых работы на активный проект
            for i in range(2):
                status = "approved" if i == 0 else "pending"
                hidden_work = HiddenWork(
                    project_id=project.id,
                    title=f"Скрытая работа #{i+1} - {project.name}",
                    description=f"Описание скрытой работы #{i+1}",
                    work_type="foundation" if i == 0 else "reinforcement",
                    location_description=f"Секция {i+1}",
                    status=status,
                    created_by_id=engineer.id,
                    approved_by_id=inspector.id if status == "approved" else None,
                    approved_at=datetime.now() - timedelta(days=5) if status == "approved" else None,
                    created_at=datetime.now() - timedelta(days=10 - i*5)
                )
                db.add(hidden_work)
                hidden_works.append(hidden_work)

    db.commit()
    print(f"Создано скрытых работ: {len(hidden_works)}")
    return hidden_works


def create_test_documents(db: Session, projects: list, users: list):
    """Создание тестовых документов"""
    print("\nСоздание тестовых документов...")

    admin = next((u for u in users if u.role == "admin"), users[0])

    documents = []
    for project in projects:
        # Создаем 2 документа на проект
        for i in range(2):
            doc_type = "contract" if i == 0 else "permit"
            document = Document(
                project_id=project.id,
                title=f"{doc_type.upper()} - {project.name}",
                description=f"Описание документа {doc_type}",
                document_type=doc_type,
                file_path=f"/uploads/documents/{project.id}/{doc_type}_{i}.pdf",
                file_size=1024000 + i * 512000,
                uploaded_by_id=admin.id,
                created_at=datetime.now() - timedelta(days=50 - i*10)
            )
            db.add(document)
            documents.append(document)

    db.commit()
    print(f"Создано документов: {len(documents)}")
    return documents


def create_test_regulations(db: Session):
    """Создание тестовых нормативов"""
    print("\nСоздание тестовых нормативов...")

    regulations_data = [
        {
            "code": "СП 70.13330.2012",
            "title": "Несущие и ограждающие конструкции",
            "category": "construction",
            "description": "Актуализированная редакция СНиП 3.03.01-87",
            "content": "Полный текст норматива...",
        },
        {
            "code": "СП 22.13330.2016",
            "title": "Основания зданий и сооружений",
            "category": "foundation",
            "description": "Актуализированная редакция СНиП 2.02.01-83*",
            "content": "Полный текст норматива...",
        },
        {
            "code": "ГОСТ 10180-2012",
            "title": "Бетоны. Методы определения прочности по контрольным образцам",
            "category": "testing",
            "description": "Методы испытаний бетона",
            "content": "Полный текст стандарта...",
        },
        {
            "code": "СП 48.13330.2019",
            "title": "Организация строительства",
            "category": "organization",
            "description": "Актуализированная редакция СНиП 12-01-2004",
            "content": "Полный текст норматива...",
        },
        {
            "code": "СП 71.13330.2017",
            "title": "Изоляционные и отделочные покрытия",
            "category": "finishing",
            "description": "Актуализированная редакция СНиП 3.04.01-87",
            "content": "Полный текст норматива...",
        },
    ]

    regulations = []
    for reg_data in regulations_data:
        # Проверяем, существует ли норматив
        existing_reg = db.query(Regulation).filter(Regulation.code == reg_data["code"]).first()
        if existing_reg:
            print(f"  Норматив {reg_data['code']} уже существует, пропускаем")
            regulations.append(existing_reg)
            continue

        regulation = Regulation(**reg_data)
        db.add(regulation)
        regulations.append(regulation)
        print(f"  Создан норматив: {reg_data['code']}")

    db.commit()
    print(f"Создано нормативов: {len(regulations)}")
    return regulations


def main():
    """Основная функция"""
    print("=" * 60)
    print("Заполнение БД тестовыми данными - ТехНадзор")
    print("=" * 60)

    db = SessionLocal()

    try:
        # Создаем данные в правильном порядке
        users = create_test_users(db)
        projects = create_test_projects(db, users)
        inspections = create_test_inspections(db, projects, users)
        hidden_works = create_test_hidden_works(db, projects, users)
        documents = create_test_documents(db, projects, users)
        regulations = create_test_regulations(db)

        print("\n" + "=" * 60)
        print("Инициализация завершена успешно!")
        print("=" * 60)
        print("\nТестовые пользователи:")
        print("  admin@tehnadzor.ru / admin123")
        print("  supervisor@tehnadzor.ru / super123")
        print("  inspector@tehnadzor.ru / inspect123")
        print("  engineer@tehnadzor.ru / eng123")
        print("  client@tehnadzor.ru / client123")
        print("\nСтатистика:")
        print(f"  Пользователей: {len(users)}")
        print(f"  Проектов: {len(projects)}")
        print(f"  Проверок: {len(inspections)}")
        print(f"  Скрытых работ: {len(hidden_works)}")
        print(f"  Документов: {len(documents)}")
        print(f"  Нормативов: {len(regulations)}")

    except Exception as e:
        print(f"\nОшибка при инициализации: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
