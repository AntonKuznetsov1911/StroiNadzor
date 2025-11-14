"""
Endpoints для экспорта данных
"""
from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List, Optional
import io
import csv
import json

from app.database import get_db
from app.models.user import User
from app.models.project import Project
from app.models.inspection import Inspection
from app.models.hidden_works import HiddenWork
from app.api.dependencies import get_current_user

router = APIRouter()


@router.get("/projects/csv")
def export_projects_csv(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Экспорт проектов в CSV"""

    projects = db.query(Project).filter(
        Project.created_by_id == current_user.id
    ).all()

    # Создаем CSV в памяти
    output = io.StringIO()
    writer = csv.writer(output)

    # Заголовки
    writer.writerow([
        'ID', 'Название', 'Тип', 'Статус', 'Адрес',
        'Дата начала', 'Дата окончания', 'Бюджет', 'Клиент'
    ])

    # Данные
    for project in projects:
        writer.writerow([
            project.id,
            project.name,
            project.project_type,
            project.status,
            project.address,
            project.start_date,
            project.end_date,
            project.budget or '',
            project.client_name or '',
        ])

    # Возвращаем CSV
    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={
            "Content-Disposition": f"attachment; filename=projects_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        }
    )


@router.get("/inspections/csv")
def export_inspections_csv(
    project_id: Optional[int] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Экспорт проверок в CSV"""

    query = db.query(Inspection).join(Project).filter(
        Project.created_by_id == current_user.id
    )

    if project_id:
        query = query.filter(Inspection.project_id == project_id)

    inspections = query.all()

    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow([
        'ID', 'Проект', 'Дата', 'Местоположение',
        'Результат', 'Широта', 'Долгота', 'Инспектор'
    ])

    for inspection in inspections:
        writer.writerow([
            inspection.id,
            inspection.project.name,
            inspection.inspection_date,
            inspection.location,
            inspection.result,
            inspection.latitude or '',
            inspection.longitude or '',
            inspection.inspector.full_name,
        ])

    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={
            "Content-Disposition": f"attachment; filename=inspections_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        }
    )


@router.get("/project/{project_id}/json")
def export_project_json(
    project_id: int,
    include_inspections: bool = True,
    include_hidden_works: bool = True,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Экспорт проекта со всеми данными в JSON"""

    project = db.query(Project).filter(
        Project.id == project_id,
        Project.created_by_id == current_user.id
    ).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    data = {
        "project": {
            "id": project.id,
            "name": project.name,
            "description": project.description,
            "project_type": project.project_type,
            "status": project.status,
            "start_date": str(project.start_date),
            "end_date": str(project.end_date) if project.end_date else None,
            "address": project.address,
            "latitude": project.latitude,
            "longitude": project.longitude,
            "client_name": project.client_name,
            "budget": project.budget,
        },
        "export_date": datetime.utcnow().isoformat(),
        "exported_by": current_user.full_name,
    }

    if include_inspections:
        inspections = db.query(Inspection).filter(
            Inspection.project_id == project_id
        ).all()

        data["inspections"] = [
            {
                "id": i.id,
                "inspection_date": str(i.inspection_date),
                "location": i.location,
                "result": i.result,
                "notes": i.notes,
                "latitude": i.latitude,
                "longitude": i.longitude,
                "inspector": i.inspector.full_name,
            }
            for i in inspections
        ]

    if include_hidden_works:
        hidden_works = db.query(HiddenWork).filter(
            HiddenWork.project_id == project_id
        ).all()

        data["hidden_works"] = [
            {
                "id": hw.id,
                "work_type": hw.work_type,
                "description": hw.description,
                "location": hw.location,
                "status": hw.status,
                "scheduled_date": str(hw.scheduled_date),
                "completed_date": str(hw.completed_date) if hw.completed_date else None,
            }
            for hw in hidden_works
        ]

    # Возвращаем JSON как файл
    json_str = json.dumps(data, ensure_ascii=False, indent=2)
    return StreamingResponse(
        iter([json_str]),
        media_type="application/json",
        headers={
            "Content-Disposition": f"attachment; filename=project_{project_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        }
    )


@router.post("/batch-export")
def batch_export(
    project_ids: List[int],
    format: str = "json",
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Пакетный экспорт нескольких проектов"""

    projects = db.query(Project).filter(
        Project.id.in_(project_ids),
        Project.created_by_id == current_user.id
    ).all()

    if not projects:
        raise HTTPException(status_code=404, detail="No projects found")

    if format == "json":
        data = {
            "export_date": datetime.utcnow().isoformat(),
            "exported_by": current_user.full_name,
            "projects": [
                {
                    "id": p.id,
                    "name": p.name,
                    "status": p.status,
                    "project_type": p.project_type,
                }
                for p in projects
            ]
        }

        json_str = json.dumps(data, ensure_ascii=False, indent=2)
        return StreamingResponse(
            iter([json_str]),
            media_type="application/json",
            headers={
                "Content-Disposition": f"attachment; filename=batch_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            }
        )

    raise HTTPException(status_code=400, detail="Unsupported format")
