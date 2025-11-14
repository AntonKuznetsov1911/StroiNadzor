"""
Скрипт для создания superuser (администратора)
"""
import sys
import os
from pathlib import Path
import getpass

# Добавляем путь к приложению
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import User
from app.security import get_password_hash


def create_superuser():
    """Создание superuser через интерактивный ввод"""
    print("=" * 60)
    print("Создание Superuser - ТехНадзор")
    print("=" * 60)
    print()

    db = SessionLocal()

    try:
        # Ввод email
        while True:
            email = input("Email: ").strip()
            if not email:
                print("Email не может быть пустым!")
                continue
            if "@" not in email or "." not in email:
                print("Введите корректный email!")
                continue

            # Проверяем, существует ли пользователь
            existing_user = db.query(User).filter(User.email == email).first()
            if existing_user:
                print(f"Пользователь с email '{email}' уже существует!")
                continue
            break

        # Ввод полного имени
        while True:
            full_name = input("Полное имя: ").strip()
            if not full_name:
                print("Полное имя не может быть пустым!")
                continue
            break

        # Ввод пароля
        while True:
            password = getpass.getpass("Пароль (минимум 6 символов): ")
            if len(password) < 6:
                print("Пароль должен содержать минимум 6 символов!")
                continue

            password_confirm = getpass.getpass("Подтвердите пароль: ")
            if password != password_confirm:
                print("Пароли не совпадают!")
                continue
            break

        # Создаем superuser
        superuser = User(
            email=email,
            full_name=full_name,
            role="admin",
            hashed_password=get_password_hash(password),
            is_active=True
        )

        db.add(superuser)
        db.commit()

        print("\n" + "=" * 60)
        print("Superuser успешно создан!")
        print("=" * 60)
        print(f"\nEmail: {email}")
        print(f"Имя: {full_name}")
        print(f"Роль: admin")
        print("\nВы можете войти в систему используя указанные данные.")

    except KeyboardInterrupt:
        print("\n\nОтменено пользователем.")
        db.rollback()
        sys.exit(1)
    except Exception as e:
        print(f"\nОшибка при создании superuser: {e}")
        db.rollback()
        raise
    finally:
        db.close()


def create_default_admin():
    """Создание администратора по умолчанию без интерактивного ввода"""
    db = SessionLocal()

    try:
        # Проверяем, существует ли админ
        existing_admin = db.query(User).filter(
            User.email == "admin@tehnadzor.ru"
        ).first()

        if existing_admin:
            print("Администратор по умолчанию уже существует!")
            print(f"Email: admin@tehnadzor.ru")
            return

        # Создаем администратора по умолчанию
        admin = User(
            email="admin@tehnadzor.ru",
            full_name="Администратор",
            role="admin",
            hashed_password=get_password_hash("admin123"),
            is_active=True
        )

        db.add(admin)
        db.commit()

        print("=" * 60)
        print("Администратор по умолчанию создан!")
        print("=" * 60)
        print("\nДанные для входа:")
        print("Email: admin@tehnadzor.ru")
        print("Пароль: admin123")
        print("\n⚠️  ВАЖНО: Смените пароль после первого входа!")

    except Exception as e:
        print(f"Ошибка при создании администратора: {e}")
        db.rollback()
        raise
    finally:
        db.close()


def main():
    """Основная функция"""
    if len(sys.argv) > 1 and sys.argv[1] == "--default":
        # Создаем админа по умолчанию
        create_default_admin()
    else:
        # Интерактивное создание
        create_superuser()


if __name__ == "__main__":
    main()
