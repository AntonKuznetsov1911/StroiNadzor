"""
Pydantic схемы для пользователей
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from app.models.user import UserRole


class UserBase(BaseModel):
    """Базовая схема пользователя"""
    email: EmailStr
    phone: Optional[str] = None
    full_name: str
    position: Optional[str] = None
    company: Optional[str] = None


class UserCreate(UserBase):
    """Схема для создания пользователя"""
    password: str = Field(..., min_length=8)
    role: UserRole = UserRole.ENGINEER


class UserUpdate(BaseModel):
    """Схема для обновления пользователя"""
    full_name: Optional[str] = None
    position: Optional[str] = None
    company: Optional[str] = None
    phone: Optional[str] = None
    avatar_url: Optional[str] = None


class UserResponse(UserBase):
    """Схема ответа с данными пользователя"""
    id: int
    role: UserRole
    avatar_url: Optional[str]
    is_active: bool
    is_verified: bool
    created_at: datetime
    last_login: Optional[datetime]

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    """Схема для входа"""
    email: EmailStr
    password: str


class Token(BaseModel):
    """Схема токена"""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
