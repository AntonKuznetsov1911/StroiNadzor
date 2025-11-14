"""
Модели базы данных
"""
from app.models.user import User
from app.models.project import Project
from app.models.inspection import Inspection, InspectionPhoto, DefectDetection
from app.models.hidden_works import HiddenWork, HiddenWorkAct
from app.models.checklist import ChecklistTemplate, Checklist, ChecklistItem
from app.models.document import Document
from app.models.material import Material, MaterialCertificate
from app.models.regulation import Regulation

__all__ = [
    "User",
    "Project",
    "Inspection",
    "InspectionPhoto",
    "DefectDetection",
    "HiddenWork",
    "HiddenWorkAct",
    "ChecklistTemplate",
    "Checklist",
    "ChecklistItem",
    "Document",
    "Material",
    "MaterialCertificate",
    "Regulation",
]
