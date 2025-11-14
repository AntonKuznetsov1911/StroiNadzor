"""
Dependencies для FastAPI endpoints
"""
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from app.database import SessionLocal
from app.models import User
from app.config import settings

# OAuth2 схема для авторизации
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_PREFIX}/auth/login")


def get_db():
    """
    Dependency для получения database сессии
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """
    Dependency для получения текущего пользователя по JWT токену

    Args:
        token: JWT токен из header Authorization
        db: Database сессия

    Returns:
        User: Текущий пользователь

    Raises:
        HTTPException: Если токен невалиден или пользователь не найден
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Декодируем JWT токен
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        user_id: str = payload.get("sub")

        if user_id is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    # Получаем пользователя из БД
    user = db.query(User).filter(User.id == int(user_id)).first()

    if user is None:
        raise credentials_exception

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )

    return user


async def get_current_user_ws(token: str) -> User:
    """
    Упрощенная версия get_current_user для WebSocket

    Args:
        token: JWT токен

    Returns:
        User: Текущий пользователь
    """
    # В реальном проекте нужно валидировать токен и получать user из БД
    # Пока возвращаем mock user
    class MockUser:
        id = 1
        role = "admin"
        is_active = True

    return MockUser()


def require_role(required_roles: list):
    """
    Dependency для проверки роли пользователя

    Args:
        required_roles: Список разрешенных ролей

    Returns:
        Функцию dependency

    Example:
        @router.get("/admin")
        async def admin_endpoint(
            user: User = Depends(require_role(["admin", "supervisor"]))
        ):
            ...
    """
    async def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in required_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Required role: {', '.join(required_roles)}"
            )
        return current_user

    return role_checker


# Предопределенные role dependencies
require_admin = require_role(["admin"])
require_supervisor = require_role(["admin", "supervisor"])
require_inspector = require_role(["admin", "supervisor", "inspector"])
require_engineer = require_role(["admin", "supervisor", "inspector", "engineer"])
