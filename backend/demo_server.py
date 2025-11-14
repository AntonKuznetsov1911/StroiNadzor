"""
Демо-сервер FastAPI для просмотра в браузере (без БД)
"""
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import io
import csv
import json
import os
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

# Инициализация OpenAI клиента (если есть API ключ)
openai_client = None
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if OPENAI_API_KEY:
    try:
        from openai import OpenAI
        openai_client = OpenAI(api_key=OPENAI_API_KEY)
        print("[OK] OpenAI client initialized")
    except ImportError:
        print("[WARNING] OpenAI library not installed. Run: pip install openai")
    except Exception as e:
        print(f"[ERROR] OpenAI initialization error: {e}")

# Создание приложения
app = FastAPI(
    title="ТехНадзор API (Demo)",
    description="API для цифрового технического надзора в строительстве - ДЕМО версия без БД",
    version="1.0.0 (Demo)",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Pydantic Models ---

class UserResponse(BaseModel):
    id: int
    email: str
    full_name: str
    role: str
    position: Optional[str] = None

class ProjectResponse(BaseModel):
    id: int
    name: str
    address: str
    status: str
    completion_percentage: float
    description: Optional[str] = None

class InspectionResponse(BaseModel):
    id: int
    project_id: int
    title: str
    status: str
    inspection_date: datetime

class HiddenWorkResponse(BaseModel):
    id: int
    project_id: int
    title: str
    work_type: str
    status: str

class RegulationResponse(BaseModel):
    id: int
    code: str
    title: str
    regulation_type: str

class AIConsultRequest(BaseModel):
    question: str
    context: Optional[str] = None

class AIConsultResponse(BaseModel):
    answer: str
    referenced_regulations: List[str]
    confidence: float

# --- Mock Data ---

MOCK_USERS = [
    {"id": 1, "email": "admin@tehnadzor.ru", "full_name": "Администратор", "role": "admin", "position": "Администратор системы"},
    {"id": 2, "email": "engineer@tehnadzor.ru", "full_name": "Иван Петров", "role": "engineer", "position": "Старший инженер"},
]

MOCK_PROJECTS = [
    {
        "id": 1,
        "name": "ЖК 'Новый горизонт'",
        "description": "Жилой комплекс на 500 квартир",
        "address": "г. Москва, Ленинский проспект, д. 123",
        "status": "in_progress",
        "completion_percentage": 68.0
    },
    {
        "id": 2,
        "name": "Торговый центр 'Галерея'",
        "description": "Торгово-развлекательный центр, 3 этажа",
        "address": "г. Санкт-Петербург, пр. Невский, д. 50",
        "status": "in_progress",
        "completion_percentage": 45.0
    }
]

MOCK_INSPECTIONS = [
    {"id": 1, "project_id": 1, "title": "Проверка качества бетона", "status": "completed", "inspection_date": datetime.now()},
    {"id": 2, "project_id": 1, "title": "Контроль арматуры 5 этаж", "status": "in_progress", "inspection_date": datetime.now()},
]

MOCK_HIDDEN_WORKS = [
    {"id": 1, "project_id": 1, "title": "Армирование фундамента", "work_type": "reinforcement", "status": "pending"},
    {"id": 2, "project_id": 1, "title": "Гидроизоляция подвала", "work_type": "waterproofing", "status": "approved"},
]

MOCK_REGULATIONS = [
    {"id": 1, "code": "СП 63.13330.2018", "title": "Бетонные и железобетонные конструкции", "regulation_type": "СП"},
    {"id": 2, "code": "СП 70.13330.2012", "title": "Несущие и ограждающие конструкции", "regulation_type": "СП"},
    {"id": 3, "code": "ГОСТ 7473-2010", "title": "Смеси бетонные. Технические условия", "regulation_type": "ГОСТ"},
]

MOCK_PHOTOS = [
    {
        "id": 1,
        "inspection_id": 1,
        "file_path": "/photos/photo1.jpg",
        "latitude": 55.751244,
        "longitude": 37.618423,
        "has_defects": True,
        "created_at": datetime.now() - timedelta(days=2)
    },
    {
        "id": 2,
        "inspection_id": 1,
        "file_path": "/photos/photo2.jpg",
        "latitude": 55.751300,
        "longitude": 37.618500,
        "has_defects": False,
        "created_at": datetime.now() - timedelta(days=1)
    },
]

MOCK_DEFECTS = [
    {
        "id": 1,
        "photo_id": 1,
        "defect_type": "crack",
        "severity": "critical",
        "confidence": 0.92,
        "description": "Трещина в бетоне, ширина ~2мм",
        "detected_at": datetime.now() - timedelta(days=2)
    },
    {
        "id": 2,
        "photo_id": 1,
        "defect_type": "deviation",
        "severity": "minor",
        "confidence": 0.85,
        "description": "Незначительное отклонение от вертикали",
        "detected_at": datetime.now() - timedelta(days=2)
    },
]

# --- Routes ---

@app.get("/")
async def root():
    """Корневой эндпоинт"""
    return {
        "message": "ТехНадзор API (Demo)",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
        "note": "Это демо-версия без подключения к базе данных. Для полной версии запустите docker-compose."
    }

@app.get("/health")
async def health_check():
    """Health check"""
    return {"status": "healthy", "service": "tehnadzor-api-demo"}

# --- Auth Endpoints ---

@app.get("/api/v1/auth/me", response_model=UserResponse, tags=["Authentication"])
async def get_current_user():
    """Получение информации о текущем пользователе (DEMO)"""
    return MOCK_USERS[1]

# --- Projects Endpoints ---

@app.get("/api/v1/projects", response_model=List[ProjectResponse], tags=["Projects"])
async def get_projects():
    """Получение списка проектов (DEMO)"""
    return MOCK_PROJECTS

@app.get("/api/v1/projects/{project_id}", response_model=ProjectResponse, tags=["Projects"])
async def get_project(project_id: int):
    """Получение проекта по ID (DEMO)"""
    for project in MOCK_PROJECTS:
        if project["id"] == project_id:
            return project
    return {"error": "Project not found"}

# --- Inspections Endpoints ---

@app.get("/api/v1/inspections", response_model=List[InspectionResponse], tags=["Inspections"])
async def get_inspections():
    """Получение списка проверок (DEMO)"""
    return MOCK_INSPECTIONS

@app.get("/api/v1/inspections/{inspection_id}", response_model=InspectionResponse, tags=["Inspections"])
async def get_inspection(inspection_id: int):
    """Получение проверки по ID (DEMO)"""
    for inspection in MOCK_INSPECTIONS:
        if inspection["id"] == inspection_id:
            return inspection
    return {"error": "Inspection not found"}

# --- Hidden Works Endpoints ---

@app.get("/api/v1/hidden-works", response_model=List[HiddenWorkResponse], tags=["Hidden Works"])
async def get_hidden_works():
    """Получение списка скрытых работ (DEMO)"""
    return MOCK_HIDDEN_WORKS

# --- Regulations Endpoints ---

@app.get("/api/v1/regulations", response_model=List[RegulationResponse], tags=["Regulations"])
async def get_regulations():
    """Получение списка нормативов (DEMO)"""
    return MOCK_REGULATIONS

@app.post("/api/v1/regulations/ai-consult", response_model=AIConsultResponse, tags=["Regulations"])
async def ai_consult(request: AIConsultRequest):
    """
    ИИ-консультант по нормативам

    Использует OpenAI API для ответов на вопросы по строительным нормативам
    """

    # Если OpenAI клиент инициализирован, используем реальный API
    if openai_client:
        try:
            # Формирование промпта с контекстом нормативов
            system_prompt = """Ты - эксперт по строительным нормативам России (СП, ГОСТ, СНиП).
Твоя задача - помогать инженерам и техническим специалистам с вопросами о строительных нормах.

Доступные нормативы:
- СП 63.13330.2018 - Бетонные и железобетонные конструкции
- СП 28.13330.2017 - Защита от коррозии
- СП 13-102-2003 - Правила обследования конструкций
- ГОСТ 23055-78 - Контроль сварки металлов
- СП 22.13330.2016 - Основания зданий и сооружений
- СП 70.13330.2012 - Несущие и ограждающие конструкции
- ГОСТ 10180-2012 - Методы определения прочности бетона
- СП 50-101-2004 - Проектирование фундаментов
- СП 48.13330.2019 - Организация строительства

Отвечай конкретно, профессионально, со ссылками на соответствующие нормативы.
"""

            user_message = request.question
            if request.context:
                user_message = f"Контекст: {request.context}\n\nВопрос: {request.question}"

            # Запрос к OpenAI API
            response = openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                max_tokens=800,
                temperature=0.7
            )

            answer = response.choices[0].message.content

            # Определение упомянутых нормативов
            referenced_regs = []
            for reg in MOCK_REGULATIONS:
                if reg["code"] in answer:
                    referenced_regs.append(reg["code"])

            # Если нормативы не упомянуты, добавляем основные
            if not referenced_regs:
                referenced_regs = ["СП 63.13330.2018", "СП 70.13330.2012"]

            return {
                "answer": answer,
                "referenced_regulations": referenced_regs,
                "confidence": 0.95
            }

        except Exception as e:
            # В случае ошибки возвращаем demo-ответ
            print(f"[ERROR] OpenAI API error: {e}")
            return {
                "answer": f"""Произошла ошибка при обращении к ИИ-консультанту: {str(e)}

Рекомендуемые нормативы для изучения:
- СП 63.13330.2018 - Бетонные и железобетонные конструкции
- СП 70.13330.2012 - Несущие и ограждающие конструкции""",
                "referenced_regulations": ["СП 63.13330.2018", "СП 70.13330.2012"],
                "confidence": 0.5
            }

    # Если OpenAI не настроен, возвращаем demo-ответ
    return {
        "answer": f"""Это демо-ответ на вопрос: "{request.question}"

[WARNING] OpenAI API не настроен. Добавьте OPENAI_API_KEY в .env файл для использования реального ИИ-консультанта.

Рекомендуемые нормативы для изучения:
- СП 63.13330.2018 - Бетонные и железобетонные конструкции
- СП 70.13330.2012 - Несущие и ограждающие конструкции""",
        "referenced_regulations": ["СП 63.13330.2018", "СП 70.13330.2012"],
        "confidence": 0.5
    }

# --- Statistics Endpoints ---

@app.get("/api/v1/stats", tags=["Statistics"])
async def get_statistics():
    """Получение статистики (DEMO)"""
    return {
        "total_projects": len(MOCK_PROJECTS),
        "total_inspections": len(MOCK_INSPECTIONS),
        "total_hidden_works": len(MOCK_HIDDEN_WORKS),
        "total_regulations": len(MOCK_REGULATIONS),
        "active_users": len(MOCK_USERS)
    }

@app.get("/api/v1/statistics/dashboard", tags=["Statistics"])
async def get_dashboard_stats():
    """Получение статистики для дашборда (DEMO)"""
    total_defects = len(MOCK_DEFECTS)
    critical_defects = sum(1 for d in MOCK_DEFECTS if d["severity"] == "critical")

    return {
        "summary": {
            "total_projects": len(MOCK_PROJECTS),
            "active_projects": sum(1 for p in MOCK_PROJECTS if p["status"] == "in_progress"),
            "total_inspections": len(MOCK_INSPECTIONS),
            "recent_inspections": len(MOCK_INSPECTIONS),
            "total_defects": total_defects,
            "critical_defects": critical_defects,
            "pending_hidden_works": sum(1 for hw in MOCK_HIDDEN_WORKS if hw["status"] == "pending"),
        },
        "projects_by_status": {
            "in_progress": sum(1 for p in MOCK_PROJECTS if p["status"] == "in_progress"),
            "planning": 0,
            "completed": 0,
        },
        "inspections_by_result": {
            "completed": sum(1 for i in MOCK_INSPECTIONS if i["status"] == "completed"),
            "in_progress": sum(1 for i in MOCK_INSPECTIONS if i["status"] == "in_progress"),
        },
    }

@app.get("/api/v1/statistics/project/{project_id}", tags=["Statistics"])
async def get_project_statistics(project_id: int):
    """Получение статистики по проекту (DEMO)"""
    project = next((p for p in MOCK_PROJECTS if p["id"] == project_id), None)
    if not project:
        return {"error": "Project not found"}

    inspections = [i for i in MOCK_INSPECTIONS if i["project_id"] == project_id]

    return {
        "project_id": project_id,
        "project_name": project["name"],
        "completion_percentage": project["completion_percentage"],
        "inspections": {
            "total": len(inspections),
            "by_result": {
                "completed": sum(1 for i in inspections if i["status"] == "completed"),
                "in_progress": sum(1 for i in inspections if i["status"] == "in_progress"),
            },
        },
        "photos": {
            "total": len(MOCK_PHOTOS),
            "with_defects": sum(1 for p in MOCK_PHOTOS if p["has_defects"]),
        },
        "defects": {
            "by_type": {
                "crack": sum(1 for d in MOCK_DEFECTS if d["defect_type"] == "crack"),
                "deviation": sum(1 for d in MOCK_DEFECTS if d["defect_type"] == "deviation"),
            },
            "by_severity": {
                "critical": sum(1 for d in MOCK_DEFECTS if d["severity"] == "critical"),
                "minor": sum(1 for d in MOCK_DEFECTS if d["severity"] == "minor"),
            },
        },
        "hidden_works": {
            "by_status": {
                "pending": 1,
                "approved": 1,
            },
        },
    }

@app.get("/api/v1/statistics/trends", tags=["Statistics"])
async def get_trends(days: int = 30):
    """Получение трендов за период (DEMO)"""
    return {
        "period_days": days,
        "inspections_trend": [
            {"date": str((datetime.now() - timedelta(days=i)).date()), "count": i % 3 + 1}
            for i in range(min(days, 7))
        ],
        "defects_trend": [
            {"date": str((datetime.now() - timedelta(days=i)).date()), "count": i % 2}
            for i in range(min(days, 7))
        ],
    }

# --- Search Endpoints ---

@app.get("/api/v1/search/global", tags=["Search"])
async def global_search(q: str = Query(..., min_length=2)):
    """Глобальный поиск по всем сущностям (DEMO)"""
    search_term = q.lower()

    # Поиск по проектам
    projects = [
        {
            "id": p["id"],
            "name": p["name"],
            "type": "project",
            "description": p.get("description", ""),
        }
        for p in MOCK_PROJECTS
        if search_term in p["name"].lower() or search_term in p.get("description", "").lower()
    ]

    # Поиск по проверкам
    inspections = [
        {
            "id": i["id"],
            "title": i["title"],
            "type": "inspection",
            "date": str(i["inspection_date"]),
        }
        for i in MOCK_INSPECTIONS
        if search_term in i["title"].lower()
    ]

    # Поиск по скрытым работам
    hidden_works = [
        {
            "id": hw["id"],
            "work_type": hw["work_type"],
            "type": "hidden_work",
            "title": hw["title"],
        }
        for hw in MOCK_HIDDEN_WORKS
        if search_term in hw["title"].lower() or search_term in hw["work_type"].lower()
    ]

    return {
        "query": q,
        "results": {
            "projects": projects,
            "inspections": inspections,
            "hidden_works": hidden_works,
            "documents": [],
        },
        "total_results": len(projects) + len(inspections) + len(hidden_works),
    }

@app.get("/api/v1/search/projects", tags=["Search"])
async def search_projects(
    q: str = Query(..., min_length=2),
    status: Optional[str] = None
):
    """Расширенный поиск по проектам (DEMO)"""
    search_term = q.lower()

    results = [
        {
            "id": p["id"],
            "name": p["name"],
            "description": p.get("description", ""),
            "status": p["status"],
            "address": p["address"],
        }
        for p in MOCK_PROJECTS
        if (search_term in p["name"].lower() or search_term in p.get("description", "").lower())
        and (status is None or p["status"] == status)
    ]

    return {
        "query": q,
        "filters": {"status": status},
        "results": results,
        "count": len(results),
    }

@app.get("/api/v1/search/regulations", tags=["Search"])
async def search_regulations(q: str = Query(..., min_length=2)):
    """Поиск по нормативным документам (DEMO)"""
    search_term = q.lower()

    results = [
        {
            "id": r["id"],
            "code": r["code"],
            "title": r["title"],
            "regulation_type": r["regulation_type"],
        }
        for r in MOCK_REGULATIONS
        if search_term in r["code"].lower() or search_term in r["title"].lower()
    ]

    return {
        "query": q,
        "results": results,
        "count": len(results),
    }

@app.get("/api/v1/search/autocomplete", tags=["Search"])
async def autocomplete(
    q: str = Query(..., min_length=1),
    entity_type: str = Query("all"),
    limit: int = Query(10, le=20)
):
    """Автодополнение для поиска (DEMO)"""
    search_term = q.lower()
    suggestions = []

    if entity_type in ["all", "projects"]:
        suggestions.extend([
            {"text": p["name"], "type": "project"}
            for p in MOCK_PROJECTS
            if p["name"].lower().startswith(search_term)
        ][:limit])

    if entity_type in ["all", "inspections"]:
        suggestions.extend([
            {"text": i["title"], "type": "inspection"}
            for i in MOCK_INSPECTIONS
            if i["title"].lower().startswith(search_term)
        ][:limit])

    return {
        "query": q,
        "suggestions": suggestions[:limit],
    }

# --- Export Endpoints ---

@app.get("/api/v1/export/projects/csv", tags=["Export"])
async def export_projects_csv():
    """Экспорт проектов в CSV (DEMO)"""
    output = io.StringIO()
    writer = csv.writer(output)

    # Заголовки
    writer.writerow(['ID', 'Название', 'Статус', 'Адрес', 'Прогресс %'])

    # Данные
    for project in MOCK_PROJECTS:
        writer.writerow([
            project["id"],
            project["name"],
            project["status"],
            project["address"],
            project["completion_percentage"],
        ])

    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={
            "Content-Disposition": f"attachment; filename=projects_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        }
    )

@app.get("/api/v1/export/inspections/csv", tags=["Export"])
async def export_inspections_csv(project_id: Optional[int] = None):
    """Экспорт проверок в CSV (DEMO)"""
    inspections = MOCK_INSPECTIONS
    if project_id:
        inspections = [i for i in inspections if i["project_id"] == project_id]

    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow(['ID', 'Проект ID', 'Название', 'Статус', 'Дата'])

    for inspection in inspections:
        writer.writerow([
            inspection["id"],
            inspection["project_id"],
            inspection["title"],
            inspection["status"],
            inspection["inspection_date"],
        ])

    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={
            "Content-Disposition": f"attachment; filename=inspections_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        }
    )

@app.get("/api/v1/export/project/{project_id}/json", tags=["Export"])
async def export_project_json(project_id: int):
    """Экспорт проекта со всеми данными в JSON (DEMO)"""
    project = next((p for p in MOCK_PROJECTS if p["id"] == project_id), None)
    if not project:
        return {"error": "Project not found"}

    data = {
        "project": project,
        "inspections": [i for i in MOCK_INSPECTIONS if i["project_id"] == project_id],
        "hidden_works": [hw for hw in MOCK_HIDDEN_WORKS if hw["project_id"] == project_id],
        "export_date": datetime.now().isoformat(),
        "exported_by": "Demo User",
    }

    json_str = json.dumps(data, ensure_ascii=False, indent=2, default=str)
    return StreamingResponse(
        iter([json_str]),
        media_type="application/json",
        headers={
            "Content-Disposition": f"attachment; filename=project_{project_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        }
    )

@app.post("/api/v1/export/batch-export", tags=["Export"])
async def batch_export(project_ids: List[int], format: str = "json"):
    """Пакетный экспорт нескольких проектов (DEMO)"""
    projects = [p for p in MOCK_PROJECTS if p["id"] in project_ids]

    if not projects:
        return {"error": "No projects found"}

    if format == "json":
        data = {
            "export_date": datetime.now().isoformat(),
            "exported_by": "Demo User",
            "projects": projects,
        }

        json_str = json.dumps(data, ensure_ascii=False, indent=2, default=str)
        return StreamingResponse(
            iter([json_str]),
            media_type="application/json",
            headers={
                "Content-Disposition": f"attachment; filename=batch_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            }
        )

    return {"error": "Unsupported format"}


if __name__ == "__main__":
    import uvicorn
    print("=" * 60)
    print("Zapusk TehNadzor Demo Server...")
    print("=" * 60)
    print("\nSwagger UI: http://localhost:8000/docs")
    print("ReDoc: http://localhost:8000/redoc")
    print("API: http://localhost:8000/api/v1")
    print("\nEto demo-versiya bez podklyucheniya k BD")
    print("Dlya polnoy versii ispolzuyte docker-compose\n")
    print("=" * 60)

    uvicorn.run(app, host="0.0.0.0", port=8000)
