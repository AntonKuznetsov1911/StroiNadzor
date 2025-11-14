"""
Главный роутер API v1
"""
from fastapi import APIRouter
from app.api.v1.endpoints import auth, projects, inspections, hidden_works, regulations, ws, documents

api_router = APIRouter()

# Подключение эндпоинтов
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(projects.router, prefix="/projects", tags=["Projects"])
api_router.include_router(inspections.router, prefix="/inspections", tags=["Inspections"])
api_router.include_router(hidden_works.router, prefix="/hidden-works", tags=["Hidden Works"])
api_router.include_router(regulations.router, prefix="/regulations", tags=["Regulations"])
api_router.include_router(documents.router, prefix="/documents", tags=["Documents"])
api_router.include_router(ws.router, tags=["WebSocket"])
