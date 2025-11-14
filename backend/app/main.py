"""
Главный файл FastAPI приложения
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from prometheus_fastapi_instrumentator import Instrumentator
from app.config import settings
from app.api.v1.router import api_router
from app.middleware import (
    RequestLoggingMiddleware,
    SecurityHeadersMiddleware,
    DatabaseSessionMiddleware
)
import os
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# Создание приложения
app = FastAPI(
    title=settings.APP_NAME,
    description="API для цифрового технического надзора в строительстве",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Custom middleware (порядок важен - они вызываются в обратном порядке!)
app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(DatabaseSessionMiddleware)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение роутеров
app.include_router(api_router, prefix=settings.API_V1_PREFIX)

# Prometheus metrics instrumentation
Instrumentator().instrument(app).expose(app, endpoint="/metrics", include_in_schema=False)

# Static files (для загруженных файлов)
if not os.path.exists("uploads"):
    os.makedirs("uploads")
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")


@app.get("/")
async def root():
    """Корневой эндпоинт"""
    return {
        "message": "ТехНадзор API",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Health check эндпоинт"""
    return {
        "status": "healthy",
        "service": "tehnadzor-api"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
