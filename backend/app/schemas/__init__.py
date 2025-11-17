"""
Pydantic schemas для всех моделей
"""
from .user import (
    UserBase,
    UserCreate,
    UserUpdate,
    UserResponse,
    UserLogin,
    Token,
    TokenData
)

from .project import (
    ProjectBase,
    ProjectCreate,
    ProjectUpdate,
    ProjectResponse,
    ProjectDetail,
    ProjectList,
    ProjectStatistics
)

from .inspection import (
    InspectionBase,
    InspectionCreate,
    InspectionUpdate,
    InspectionResponse,
    InspectionDetail,
    InspectionList,
    InspectionPhotoResponse,
    DefectDetectionResponse
)

from .hidden_work import (
    HiddenWorkType,
    HiddenWorkStatus,
    HiddenWorkBase,
    HiddenWorkCreate,
    HiddenWorkUpdate,
    HiddenWorkResponse,
    HiddenWorkDetail,
    HiddenWorkList,
    HiddenWorkActBase,
    HiddenWorkActCreate,
    HiddenWorkActUpdate,
    HiddenWorkActResponse
)

from .document import (
    DocumentType,
    DocumentStatus,
    DocumentBase,
    DocumentCreate,
    DocumentUpdate,
    DocumentResponse,
    DocumentDetail,
    DocumentList,
    DocumentUpload,
    DocumentDownloadResponse
)

from .regulation import (
    RegulationType,
    RegulationCategory,
    RegulationBase,
    RegulationCreate,
    RegulationUpdate,
    RegulationResponse,
    RegulationDetail,
    RegulationList,
    RegulationSearch,
    RegulationSearchResult,
    RegulationAIQuery,
    RegulationAIResponse
)

from .checklist import (
    ChecklistStatus,
    CheckItemStatus,
    Priority,
    ChecklistTemplateBase,
    ChecklistTemplateCreate,
    ChecklistTemplateUpdate,
    ChecklistTemplateResponse,
    ChecklistTemplateDetail,
    ChecklistBase,
    ChecklistCreate,
    ChecklistUpdate,
    ChecklistResponse,
    ChecklistDetail,
    ChecklistList,
    ChecklistStatistics,
    ChecklistItemResponse,
    ChecklistItemUpdate
)

from .material import (
    MaterialBase,
    MaterialCreate,
    MaterialUpdate,
    MaterialResponse,
    MaterialDetail,
    MaterialList,
    MaterialStatistics,
    MaterialInventory,
    MaterialCertificateBase,
    MaterialCertificateCreate,
    MaterialCertificateUpdate,
    MaterialCertificateResponse
)

__all__ = [
    # User
    "UserBase", "UserCreate", "UserUpdate", "UserResponse",
    "UserLogin", "Token", "TokenData",

    # Project
    "ProjectBase", "ProjectCreate", "ProjectUpdate", "ProjectResponse",
    "ProjectDetail", "ProjectList", "ProjectStatistics",

    # Inspection
    "InspectionBase", "InspectionCreate", "InspectionUpdate", "InspectionResponse",
    "InspectionDetail", "InspectionList", "InspectionPhotoResponse", "DefectDetectionResponse",

    # Hidden Work
    "HiddenWorkType", "HiddenWorkStatus",
    "HiddenWorkBase", "HiddenWorkCreate", "HiddenWorkUpdate", "HiddenWorkResponse",
    "HiddenWorkDetail", "HiddenWorkList",
    "HiddenWorkActBase", "HiddenWorkActCreate", "HiddenWorkActUpdate", "HiddenWorkActResponse",

    # Document
    "DocumentType", "DocumentStatus",
    "DocumentBase", "DocumentCreate", "DocumentUpdate", "DocumentResponse",
    "DocumentDetail", "DocumentList", "DocumentUpload", "DocumentDownloadResponse",

    # Regulation
    "RegulationType", "RegulationCategory",
    "RegulationBase", "RegulationCreate", "RegulationUpdate", "RegulationResponse",
    "RegulationDetail", "RegulationList",
    "RegulationSearch", "RegulationSearchResult",
    "RegulationAIQuery", "RegulationAIResponse",

    # Checklist
    "ChecklistStatus", "CheckItemStatus", "Priority",
    "ChecklistTemplateBase", "ChecklistTemplateCreate", "ChecklistTemplateUpdate",
    "ChecklistTemplateResponse", "ChecklistTemplateDetail",
    "ChecklistBase", "ChecklistCreate", "ChecklistUpdate", "ChecklistResponse",
    "ChecklistDetail", "ChecklistList", "ChecklistStatistics",
    "ChecklistItemResponse", "ChecklistItemUpdate",

    # Material
    "MaterialBase", "MaterialCreate", "MaterialUpdate", "MaterialResponse",
    "MaterialDetail", "MaterialList", "MaterialStatistics", "MaterialInventory",
    "MaterialCertificateBase", "MaterialCertificateCreate", "MaterialCertificateUpdate",
    "MaterialCertificateResponse",
]
