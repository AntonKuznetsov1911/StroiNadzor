"""
Эндпоинты для работы со скрытыми работами (Модуль 2 MVP)
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.database import get_db
from app.models.user import User
from app.models.hidden_works import HiddenWork, HiddenWorkAct, HiddenWorkStatus
from app.api.v1.endpoints.auth import get_current_user
from pydantic import BaseModel
from typing import Optional

router = APIRouter()


# Pydantic схемы для скрытых работ
class HiddenWorkCreate(BaseModel):
    project_id: int
    title: str
    description: Optional[str] = None
    work_type: str
    floor_level: Optional[str] = None
    section: Optional[str] = None
    planned_inspection_date: Optional[datetime] = None


class HiddenWorkResponse(BaseModel):
    id: int
    project_id: int
    title: str
    description: Optional[str]
    work_type: str
    status: str
    floor_level: Optional[str]
    section: Optional[str]
    planned_inspection_date: Optional[datetime]
    created_at: datetime

    class Config:
        from_attributes = True


class HiddenWorkActCreate(BaseModel):
    act_number: str
    contractor_representative: Optional[str] = None
    technical_supervision: Optional[str] = None
    is_approved: bool
    comments: Optional[str] = None
    defects_found: Optional[str] = None


class HiddenWorkActResponse(BaseModel):
    id: int
    hidden_work_id: int
    act_number: str
    act_date: datetime
    is_approved: bool
    comments: Optional[str]
    document_url: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


@router.post("/", response_model=HiddenWorkResponse, status_code=status.HTTP_201_CREATED)
async def create_hidden_work(
    work_data: HiddenWorkCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Создание записи о скрытых работах"""
    db_work = HiddenWork(**work_data.model_dump())

    db.add(db_work)
    db.commit()
    db.refresh(db_work)

    return db_work


@router.get("/", response_model=List[HiddenWorkResponse])
async def get_hidden_works(
    project_id: Optional[int] = None,
    status: Optional[HiddenWorkStatus] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Получение списка скрытых работ"""
    query = db.query(HiddenWork)

    if project_id:
        query = query.filter(HiddenWork.project_id == project_id)
    if status:
        query = query.filter(HiddenWork.status == status)

    works = query.all()
    return works


@router.get("/{work_id}", response_model=HiddenWorkResponse)
async def get_hidden_work(
    work_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Получение скрытых работ по ID"""
    work = db.query(HiddenWork).filter(HiddenWork.id == work_id).first()

    if not work:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Hidden work not found"
        )

    return work


@router.post("/{work_id}/acts", response_model=HiddenWorkActResponse, status_code=status.HTTP_201_CREATED)
async def create_hidden_work_act(
    work_id: int,
    act_data: HiddenWorkActCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Создание акта освидетельствования скрытых работ
    С обязательной фотофиксацией перед закрытием работ
    """
    work = db.query(HiddenWork).filter(HiddenWork.id == work_id).first()

    if not work:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Hidden work not found"
        )

    db_act = HiddenWorkAct(
        hidden_work_id=work_id,
        inspector_id=current_user.id,
        **act_data.model_dump()
    )

    db.add(db_act)

    # Обновление статуса скрытых работ
    if act_data.is_approved:
        work.status = HiddenWorkStatus.APPROVED
    else:
        work.status = HiddenWorkStatus.REJECTED

    db.commit()
    db.refresh(db_act)

    return db_act


@router.get("/{work_id}/acts", response_model=List[HiddenWorkActResponse])
async def get_hidden_work_acts(
    work_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Получение актов для скрытых работ"""
    work = db.query(HiddenWork).filter(HiddenWork.id == work_id).first()

    if not work:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Hidden work not found"
        )

    return work.acts
