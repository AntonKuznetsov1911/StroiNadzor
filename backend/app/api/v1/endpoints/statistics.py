"""
Endpoints для статистики
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from datetime import datetime, timedelta
from typing import List, Dict, Any

from app.database import get_db
from app.models.user import User
from app.models.project import Project
from app.models.inspection import Inspection, InspectionPhoto, DefectDetection
from app.models.hidden_works import HiddenWork
from app.api.dependencies import get_current_user

router = APIRouter()


@router.get("/dashboard")
def get_dashboard_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Получение статистики для дашборда"""

    # Общая статистика
    total_projects = db.query(Project).filter(
        Project.created_by_id == current_user.id
    ).count()

    active_projects = db.query(Project).filter(
        and_(
            Project.created_by_id == current_user.id,
            Project.status == 'in_progress'
        )
    ).count()

    total_inspections = db.query(Inspection).join(Project).filter(
        Project.created_by_id == current_user.id
    ).count()

    # Проверки за последние 30 дней
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    recent_inspections = db.query(Inspection).join(Project).filter(
        and_(
            Project.created_by_id == current_user.id,
            Inspection.created_at >= thirty_days_ago
        )
    ).count()

    # Дефекты
    total_defects = db.query(DefectDetection).join(InspectionPhoto).join(Inspection).join(Project).filter(
        Project.created_by_id == current_user.id
    ).count()

    critical_defects = db.query(DefectDetection).join(InspectionPhoto).join(Inspection).join(Project).filter(
        and_(
            Project.created_by_id == current_user.id,
            DefectDetection.severity == 'critical'
        )
    ).count()

    # Скрытые работы
    pending_hidden_works = db.query(HiddenWork).join(Project).filter(
        and_(
            Project.created_by_id == current_user.id,
            HiddenWork.status == 'pending'
        )
    ).count()

    # Статистика по проектам
    projects_by_status = db.query(
        Project.status,
        func.count(Project.id)
    ).filter(
        Project.created_by_id == current_user.id
    ).group_by(Project.status).all()

    # Проверки по результатам
    inspections_by_result = db.query(
        Inspection.result,
        func.count(Inspection.id)
    ).join(Project).filter(
        Project.created_by_id == current_user.id
    ).group_by(Inspection.result).all()

    return {
        "summary": {
            "total_projects": total_projects,
            "active_projects": active_projects,
            "total_inspections": total_inspections,
            "recent_inspections": recent_inspections,
            "total_defects": total_defects,
            "critical_defects": critical_defects,
            "pending_hidden_works": pending_hidden_works,
        },
        "projects_by_status": {
            status: count for status, count in projects_by_status
        },
        "inspections_by_result": {
            result: count for result, count in inspections_by_result
        },
    }


@router.get("/project/{project_id}")
def get_project_statistics(
    project_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Получение статистики по проекту"""

    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Проверки
    total_inspections = db.query(Inspection).filter(
        Inspection.project_id == project_id
    ).count()

    inspections_by_result = db.query(
        Inspection.result,
        func.count(Inspection.id)
    ).filter(
        Inspection.project_id == project_id
    ).group_by(Inspection.result).all()

    # Фотографии
    total_photos = db.query(InspectionPhoto).join(Inspection).filter(
        Inspection.project_id == project_id
    ).count()

    photos_with_defects = db.query(InspectionPhoto).join(Inspection).filter(
        and_(
            Inspection.project_id == project_id,
            InspectionPhoto.has_defects == True
        )
    ).count()

    # Дефекты
    defects_by_type = db.query(
        DefectDetection.defect_type,
        func.count(DefectDetection.id)
    ).join(InspectionPhoto).join(Inspection).filter(
        Inspection.project_id == project_id
    ).group_by(DefectDetection.defect_type).all()

    defects_by_severity = db.query(
        DefectDetection.severity,
        func.count(DefectDetection.id)
    ).join(InspectionPhoto).join(Inspection).filter(
        Inspection.project_id == project_id
    ).group_by(DefectDetection.severity).all()

    # Скрытые работы
    hidden_works_by_status = db.query(
        HiddenWork.status,
        func.count(HiddenWork.id)
    ).filter(
        HiddenWork.project_id == project_id
    ).group_by(HiddenWork.status).all()

    # Прогресс проекта (пример расчета)
    completion_percentage = 0
    if project.end_date:
        total_days = (project.end_date - project.start_date).days
        elapsed_days = (datetime.utcnow().date() - project.start_date).days
        completion_percentage = min(100, max(0, (elapsed_days / total_days) * 100))

    return {
        "project_id": project_id,
        "project_name": project.name,
        "completion_percentage": round(completion_percentage, 2),
        "inspections": {
            "total": total_inspections,
            "by_result": {result: count for result, count in inspections_by_result},
        },
        "photos": {
            "total": total_photos,
            "with_defects": photos_with_defects,
        },
        "defects": {
            "by_type": {dtype: count for dtype, count in defects_by_type},
            "by_severity": {severity: count for severity, count in defects_by_severity},
        },
        "hidden_works": {
            "by_status": {status: count for status, count in hidden_works_by_status},
        },
    }


@router.get("/trends")
def get_trends(
    days: int = 30,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Получение трендов за период"""

    start_date = datetime.utcnow() - timedelta(days=days)

    # Проверки по дням
    inspections_by_day = db.query(
        func.date(Inspection.inspection_date).label('date'),
        func.count(Inspection.id).label('count')
    ).join(Project).filter(
        and_(
            Project.created_by_id == current_user.id,
            Inspection.inspection_date >= start_date
        )
    ).group_by(func.date(Inspection.inspection_date)).all()

    # Дефекты по дням
    defects_by_day = db.query(
        func.date(DefectDetection.detected_at).label('date'),
        func.count(DefectDetection.id).label('count')
    ).join(InspectionPhoto).join(Inspection).join(Project).filter(
        and_(
            Project.created_by_id == current_user.id,
            DefectDetection.detected_at >= start_date
        )
    ).group_by(func.date(DefectDetection.detected_at)).all()

    return {
        "period_days": days,
        "inspections_trend": [
            {"date": str(date), "count": count}
            for date, count in inspections_by_day
        ],
        "defects_trend": [
            {"date": str(date), "count": count}
            for date, count in defects_by_day
        ],
    }


@router.get("/export-stats")
def export_statistics(
    project_id: int = None,
    format: str = "json",
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Экспорт статистики в различных форматах"""

    if project_id:
        stats = get_project_statistics(project_id, current_user, db)
    else:
        stats = get_dashboard_stats(current_user, db)

    if format == "json":
        return stats
    elif format == "csv":
        # TODO: Конвертировать в CSV
        return {"message": "CSV export not implemented yet", "data": stats}
    elif format == "pdf":
        # TODO: Генерация PDF отчета
        return {"message": "PDF export not implemented yet", "data": stats}
    else:
        raise HTTPException(status_code=400, detail="Unsupported format")
