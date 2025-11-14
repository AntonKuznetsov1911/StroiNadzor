"""
Endpoints для поиска
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, func
from typing import List, Optional

from app.database import get_db
from app.models.user import User
from app.models.project import Project
from app.models.inspection import Inspection
from app.models.hidden_works import HiddenWork
from app.models.document import Document
from app.models.regulation import Regulation
from app.api.dependencies import get_current_user

router = APIRouter()


@router.get("/global")
def global_search(
    q: str = Query(..., min_length=2, description="Поисковый запрос"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Глобальный поиск по всем сущностям"""

    search_term = f"%{q}%"

    # Поиск проектов
    projects = db.query(Project).filter(
        and_(
            Project.created_by_id == current_user.id,
            or_(
                Project.name.ilike(search_term),
                Project.description.ilike(search_term),
                Project.address.ilike(search_term)
            )
        )
    ).limit(10).all()

    # Поиск проверок
    inspections = db.query(Inspection).join(Project).filter(
        and_(
            Project.created_by_id == current_user.id,
            or_(
                Inspection.location.ilike(search_term),
                Inspection.notes.ilike(search_term)
            )
        )
    ).limit(10).all()

    # Поиск скрытых работ
    hidden_works = db.query(HiddenWork).join(Project).filter(
        and_(
            Project.created_by_id == current_user.id,
            or_(
                HiddenWork.work_type.ilike(search_term),
                HiddenWork.description.ilike(search_term),
                HiddenWork.location.ilike(search_term)
            )
        )
    ).limit(10).all()

    # Поиск документов
    documents = db.query(Document).join(Project).filter(
        and_(
            Project.created_by_id == current_user.id,
            or_(
                Document.title.ilike(search_term),
                Document.description.ilike(search_term)
            )
        )
    ).limit(10).all()

    return {
        "query": q,
        "results": {
            "projects": [
                {
                    "id": p.id,
                    "name": p.name,
                    "type": "project",
                    "description": p.description,
                }
                for p in projects
            ],
            "inspections": [
                {
                    "id": i.id,
                    "location": i.location,
                    "type": "inspection",
                    "date": str(i.inspection_date),
                }
                for i in inspections
            ],
            "hidden_works": [
                {
                    "id": hw.id,
                    "work_type": hw.work_type,
                    "type": "hidden_work",
                    "location": hw.location,
                }
                for hw in hidden_works
            ],
            "documents": [
                {
                    "id": d.id,
                    "title": d.title,
                    "type": "document",
                    "document_type": d.document_type,
                }
                for d in documents
            ],
        },
        "total_results": len(projects) + len(inspections) + len(hidden_works) + len(documents),
    }


@router.get("/projects")
def search_projects(
    q: str = Query(..., min_length=2),
    project_type: Optional[str] = None,
    status: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Расширенный поиск по проектам"""

    search_term = f"%{q}%"

    query = db.query(Project).filter(
        and_(
            Project.created_by_id == current_user.id,
            or_(
                Project.name.ilike(search_term),
                Project.description.ilike(search_term),
                Project.address.ilike(search_term),
                Project.client_name.ilike(search_term)
            )
        )
    )

    if project_type:
        query = query.filter(Project.project_type == project_type)

    if status:
        query = query.filter(Project.status == status)

    projects = query.all()

    return {
        "query": q,
        "filters": {
            "project_type": project_type,
            "status": status,
        },
        "results": [
            {
                "id": p.id,
                "name": p.name,
                "description": p.description,
                "project_type": p.project_type,
                "status": p.status,
                "address": p.address,
                "client_name": p.client_name,
            }
            for p in projects
        ],
        "count": len(projects),
    }


@router.get("/regulations")
def search_regulations(
    q: str = Query(..., min_length=2, description="Поиск по СП, ГОСТ"),
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Поиск по нормативным документам"""

    search_term = f"%{q}%"

    query = db.query(Regulation).filter(
        or_(
            Regulation.code.ilike(search_term),
            Regulation.title.ilike(search_term),
            Regulation.content.ilike(search_term)
        )
    )

    if category:
        query = query.filter(Regulation.category == category)

    regulations = query.limit(20).all()

    return {
        "query": q,
        "category": category,
        "results": [
            {
                "id": r.id,
                "code": r.code,
                "title": r.title,
                "category": r.category,
                "effective_date": str(r.effective_date) if r.effective_date else None,
            }
            for r in regulations
        ],
        "count": len(regulations),
    }


@router.get("/autocomplete")
def autocomplete(
    q: str = Query(..., min_length=1),
    entity_type: str = Query("all", description="Тип сущности: all, projects, inspections, documents"),
    limit: int = Query(10, le=20),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Автодополнение для поиска"""

    search_term = f"{q}%"
    suggestions = []

    if entity_type in ["all", "projects"]:
        projects = db.query(Project.name).filter(
            and_(
                Project.created_by_id == current_user.id,
                Project.name.ilike(search_term)
            )
        ).limit(limit).all()
        suggestions.extend([{"text": p[0], "type": "project"} for p in projects])

    if entity_type in ["all", "inspections"]:
        locations = db.query(Inspection.location).join(Project).filter(
            and_(
                Project.created_by_id == current_user.id,
                Inspection.location.ilike(search_term)
            )
        ).distinct().limit(limit).all()
        suggestions.extend([{"text": l[0], "type": "location"} for l in locations])

    if entity_type in ["all", "documents"]:
        docs = db.query(Document.title).join(Project).filter(
            and_(
                Project.created_by_id == current_user.id,
                Document.title.ilike(search_term)
            )
        ).limit(limit).all()
        suggestions.extend([{"text": d[0], "type": "document"} for d in docs])

    return {
        "query": q,
        "suggestions": suggestions[:limit],
    }
