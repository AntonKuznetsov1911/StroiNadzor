#!/usr/bin/env python3
"""
CLI утилита для управления приложением StroiNadzor
"""
import asyncio
import sys
import click
from pathlib import Path
from datetime import datetime, timedelta

# Добавляем путь к приложению
sys.path.append(str(Path(__file__).parent))

from sqlalchemy import text
from app.core.database import async_session_maker, engine, Base
from app.core.security import get_password_hash
from app.models import User, Project, Inspection, Material, Document


@click.group()
def cli():
    """StroiNadzor - Система строительного надзора"""
    pass


@cli.group()
def db():
    """Команды для работы с базой данных"""
    pass


@db.command()
def init():
    """Инициализация базы данных (создание таблиц)"""
    async def _init():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        click.echo("✅ База данных инициализирована")

    asyncio.run(_init())


@db.command()
@click.option('--yes', '-y', is_flag=True, help='Подтвердить без запроса')
def reset(yes):
    """Сброс базы данных (удаление всех таблиц)"""
    if not yes:
        click.confirm('⚠️  Это удалит ВСЕ данные. Продолжить?', abort=True)

    async def _reset():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
        click.echo("✅ База данных сброшена")

    asyncio.run(_reset())


@db.command()
def seed():
    """Заполнение базы данных тестовыми данными"""
    import subprocess
    result = subprocess.run([sys.executable, "seed_data.py"], cwd=Path(__file__).parent)
    if result.returncode == 0:
        click.echo("✅ Данные успешно загружены")
    else:
        click.echo("❌ Ошибка при загрузке данных", err=True)


@db.command()
def status():
    """Статус базы данных"""
    async def _status():
        try:
            async with async_session_maker() as session:
                # Проверяем подключение
                await session.execute(text("SELECT 1"))

                # Статистика
                users_count = await session.scalar(text("SELECT COUNT(*) FROM users"))
                projects_count = await session.scalar(text("SELECT COUNT(*) FROM projects"))
                inspections_count = await session.scalar(text("SELECT COUNT(*) FROM inspections"))
                materials_count = await session.scalar(text("SELECT COUNT(*) FROM materials"))
                documents_count = await session.scalar(text("SELECT COUNT(*) FROM documents"))

                click.echo("\n" + "=" * 50)
                click.echo("📊 Статус базы данных")
                click.echo("=" * 50)
                click.echo(f"✅ Подключение: Активно")
                click.echo(f"\nЗаписи:")
                click.echo(f"  • Пользователи:      {users_count or 0}")
                click.echo(f"  • Проекты:           {projects_count or 0}")
                click.echo(f"  • Осмотры:           {inspections_count or 0}")
                click.echo(f"  • Материалы:         {materials_count or 0}")
                click.echo(f"  • Документы:         {documents_count or 0}")
                click.echo("=" * 50 + "\n")

        except Exception as e:
            click.echo(f"❌ Ошибка подключения: {e}", err=True)

    asyncio.run(_status())


@db.command()
def backup():
    """Создание резервной копии БД (только для SQLite)"""
    import shutil
    from app.core.config import settings

    if "sqlite" in settings.DATABASE_URL:
        db_file = settings.DATABASE_URL.replace("sqlite:///", "")
        backup_file = f"{db_file}.backup.{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        shutil.copy2(db_file, backup_file)
        click.echo(f"✅ Резервная копия создана: {backup_file}")
    else:
        click.echo("❌ Команда работает только с SQLite", err=True)


@cli.group()
def user():
    """Команды для работы с пользователями"""
    pass


@user.command()
@click.option('--username', '-u', required=True, help='Имя пользователя')
@click.option('--email', '-e', required=True, help='Email')
@click.option('--password', '-p', required=True, help='Пароль')
@click.option('--role', '-r', type=click.Choice(['admin', 'supervisor', 'engineer', 'inspector']), default='engineer')
@click.option('--full-name', '-n', required=True, help='Полное имя')
def create(username, email, password, role, full_name):
    """Создание нового пользователя"""
    async def _create():
        async with async_session_maker() as session:
            # Проверяем существование
            existing = await session.scalar(
                text("SELECT id FROM users WHERE username = :username OR email = :email"),
                {"username": username, "email": email}
            )
            if existing:
                click.echo("❌ Пользователь с таким username или email уже существует", err=True)
                return

            user = User(
                username=username,
                email=email,
                hashed_password=get_password_hash(password),
                full_name=full_name,
                role=role,
                is_active=True,
            )
            session.add(user)
            await session.commit()

            click.echo(f"✅ Пользователь создан:")
            click.echo(f"  • Username: {username}")
            click.echo(f"  • Email: {email}")
            click.echo(f"  • Role: {role}")

    asyncio.run(_create())


@user.command()
def list():
    """Список всех пользователей"""
    async def _list():
        async with async_session_maker() as session:
            result = await session.execute(
                text("SELECT id, username, email, role, is_active, created_at FROM users ORDER BY created_at DESC")
            )
            users = result.fetchall()

            if not users:
                click.echo("Пользователи не найдены")
                return

            click.echo("\n" + "=" * 100)
            click.echo(f"{'ID':<5} {'Username':<15} {'Email':<30} {'Role':<12} {'Active':<8} {'Created':<20}")
            click.echo("=" * 100)

            for user in users:
                active = "✅" if user[4] else "❌"
                created = user[5].strftime("%Y-%m-%d %H:%M") if user[5] else "N/A"
                click.echo(f"{user[0]:<5} {user[1]:<15} {user[2]:<30} {user[3]:<12} {active:<8} {created:<20}")

            click.echo("=" * 100 + "\n")

    asyncio.run(_list())


@user.command()
@click.argument('username')
@click.option('--yes', '-y', is_flag=True, help='Подтвердить без запроса')
def delete(username, yes):
    """Удаление пользователя"""
    if not yes:
        click.confirm(f'⚠️  Удалить пользователя {username}?', abort=True)

    async def _delete():
        async with async_session_maker() as session:
            result = await session.execute(
                text("DELETE FROM users WHERE username = :username"),
                {"username": username}
            )
            await session.commit()

            if result.rowcount > 0:
                click.echo(f"✅ Пользователь {username} удалён")
            else:
                click.echo(f"❌ Пользователь {username} не найден", err=True)

    asyncio.run(_delete())


@user.command()
@click.argument('username')
@click.option('--password', '-p', required=True, help='Новый пароль')
def reset_password(username, password):
    """Сброс пароля пользователя"""
    async def _reset_password():
        async with async_session_maker() as session:
            hashed = get_password_hash(password)
            result = await session.execute(
                text("UPDATE users SET hashed_password = :hashed WHERE username = :username"),
                {"hashed": hashed, "username": username}
            )
            await session.commit()

            if result.rowcount > 0:
                click.echo(f"✅ Пароль для {username} обновлён")
            else:
                click.echo(f"❌ Пользователь {username} не найден", err=True)

    asyncio.run(_reset_password())


@cli.group()
def project():
    """Команды для работы с проектами"""
    pass


@project.command()
def list():
    """Список всех проектов"""
    async def _list():
        async with async_session_maker() as session:
            result = await session.execute(
                text("SELECT id, name, status, start_date, end_date, budget FROM projects ORDER BY created_at DESC LIMIT 20")
            )
            projects = result.fetchall()

            if not projects:
                click.echo("Проекты не найдены")
                return

            click.echo("\n" + "=" * 120)
            click.echo(f"{'ID':<5} {'Name':<50} {'Status':<15} {'Start':<12} {'End':<12} {'Budget':<15}")
            click.echo("=" * 120)

            for proj in projects:
                budget = f"{proj[5]:,.2f}" if proj[5] else "N/A"
                start = proj[3].strftime("%Y-%m-%d") if proj[3] else "N/A"
                end = proj[4].strftime("%Y-%m-%d") if proj[4] else "N/A"
                name = proj[1][:48] + ".." if len(proj[1]) > 50 else proj[1]
                click.echo(f"{proj[0]:<5} {name:<50} {proj[2]:<15} {start:<12} {end:<12} {budget:<15}")

            click.echo("=" * 120 + "\n")

    asyncio.run(_list())


@project.command()
@click.argument('project_id', type=int)
def info(project_id):
    """Детальная информация о проекте"""
    async def _info():
        async with async_session_maker() as session:
            # Проект
            result = await session.execute(
                text("SELECT * FROM projects WHERE id = :id"),
                {"id": project_id}
            )
            project = result.fetchone()

            if not project:
                click.echo(f"❌ Проект #{project_id} не найден", err=True)
                return

            # Статистика
            inspections = await session.scalar(
                text("SELECT COUNT(*) FROM inspections WHERE project_id = :id"),
                {"id": project_id}
            )
            materials = await session.scalar(
                text("SELECT COUNT(*) FROM materials WHERE project_id = :id"),
                {"id": project_id}
            )
            documents = await session.scalar(
                text("SELECT COUNT(*) FROM documents WHERE project_id = :id"),
                {"id": project_id}
            )

            click.echo("\n" + "=" * 80)
            click.echo(f"📋 Проект #{project_id}")
            click.echo("=" * 80)
            click.echo(f"Название:     {project[1]}")
            click.echo(f"Статус:       {project[7]}")
            click.echo(f"Адрес:        {project[3]}")
            click.echo(f"Заказчик:     {project[4]}")
            click.echo(f"Подрядчик:    {project[5]}")
            click.echo(f"Период:       {project[8]} - {project[9]}")
            click.echo(f"Бюджет:       {project[10]:,.2f} руб.")
            click.echo(f"\nСтатистика:")
            click.echo(f"  • Осмотры:      {inspections or 0}")
            click.echo(f"  • Материалы:    {materials or 0}")
            click.echo(f"  • Документы:    {documents or 0}")
            click.echo("=" * 80 + "\n")

    asyncio.run(_info())


@cli.command()
def stats():
    """Общая статистика системы"""
    async def _stats():
        async with async_session_maker() as session:
            # Подсчёты
            users = await session.scalar(text("SELECT COUNT(*) FROM users"))
            projects_total = await session.scalar(text("SELECT COUNT(*) FROM projects"))
            projects_active = await session.scalar(text("SELECT COUNT(*) FROM projects WHERE status = 'in_progress'"))
            inspections = await session.scalar(text("SELECT COUNT(*) FROM inspections"))
            materials = await session.scalar(text("SELECT COUNT(*) FROM materials"))
            documents = await session.scalar(text("SELECT COUNT(*) FROM documents"))

            # Недавняя активность
            recent_inspections = await session.scalar(
                text("SELECT COUNT(*) FROM inspections WHERE inspection_date >= :date"),
                {"date": datetime.now().date() - timedelta(days=7)}
            )

            click.echo("\n" + "=" * 60)
            click.echo("📊 Статистика системы StroiNadzor")
            click.echo("=" * 60)
            click.echo(f"\n👥 Пользователи:              {users or 0}")
            click.echo(f"📁 Проекты:                   {projects_total or 0}")
            click.echo(f"   └─ Активные:               {projects_active or 0}")
            click.echo(f"🔍 Осмотры:                   {inspections or 0}")
            click.echo(f"   └─ За последние 7 дней:    {recent_inspections or 0}")
            click.echo(f"📦 Материалы:                 {materials or 0}")
            click.echo(f"📄 Документы:                 {documents or 0}")
            click.echo("=" * 60 + "\n")

    asyncio.run(_stats())


@cli.command()
def version():
    """Версия приложения"""
    click.echo("\n" + "=" * 60)
    click.echo("StroiNadzor - Система строительного надзора")
    click.echo("=" * 60)
    click.echo("Версия:       1.0.0")
    click.echo("Python:       " + sys.version.split()[0])
    click.echo("Дата:         2025-01-17")
    click.echo("=" * 60 + "\n")


if __name__ == "__main__":
    cli()
