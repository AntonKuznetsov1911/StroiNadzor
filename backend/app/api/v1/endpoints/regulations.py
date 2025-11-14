"""
Эндпоинты для работы с нормативами и ИИ-консультантом (Модуль 3 MVP)
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel

from app.database import get_db
from app.models.user import User
from app.models.regulation import Regulation
from app.api.v1.endpoints.auth import get_current_user
from app.config import settings

# Для ИИ консультанта
try:
    from openai import OpenAI
    openai_available = True
except ImportError:
    openai_available = False

try:
    import anthropic
    claude_available = True
except ImportError:
    claude_available = False

router = APIRouter()


# Pydantic схемы
class RegulationResponse(BaseModel):
    id: int
    code: str
    title: str
    regulation_type: str
    description: Optional[str]
    is_active: bool

    class Config:
        from_attributes = True


class AIConsultRequest(BaseModel):
    question: str
    context: Optional[str] = None  # Контекст проекта, этапа и т.д.


class AIConsultResponse(BaseModel):
    answer: str
    referenced_regulations: List[str]
    confidence: float


@router.get("/", response_model=List[RegulationResponse])
async def get_regulations(
    search: Optional[str] = Query(None, description="Поиск по коду или названию"),
    regulation_type: Optional[str] = Query(None, description="Фильтр по типу (СП, ГОСТ и т.д.)"),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Получение списка нормативов"""
    query = db.query(Regulation).filter(Regulation.is_active == True)

    if search:
        query = query.filter(
            (Regulation.code.ilike(f"%{search}%")) |
            (Regulation.title.ilike(f"%{search}%"))
        )

    if regulation_type:
        query = query.filter(Regulation.regulation_type == regulation_type)

    regulations = query.offset(skip).limit(limit).all()
    return regulations


@router.get("/{regulation_id}", response_model=RegulationResponse)
async def get_regulation(
    regulation_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Получение норматива по ID"""
    regulation = db.query(Regulation).filter(Regulation.id == regulation_id).first()

    if not regulation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Regulation not found"
        )

    return regulation


@router.post("/ai-consult", response_model=AIConsultResponse)
async def ai_consult(
    request: AIConsultRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    ИИ-консультант по нормативам
    Использует OpenAI API или Claude API для ответов на вопросы
    """

    # Получение релевантных нормативов из БД
    # В продакшене здесь будет использоваться Elasticsearch для семантического поиска
    relevant_regulations = db.query(Regulation).filter(Regulation.is_active == True).limit(5).all()

    # Формирование контекста для ИИ
    regulations_context = "\n".join([
        f"- {reg.code}: {reg.title}"
        for reg in relevant_regulations
    ])

    prompt = f"""
Ты - эксперт по строительным нормативам и правилам России.

Доступные нормативы:
{regulations_context}

Контекст проекта: {request.context or 'Не указан'}

Вопрос: {request.question}

Предоставь подробный ответ со ссылками на конкретные нормативы.
"""

    try:
        # Использование Claude API (приоритет)
        if claude_available and settings.CLAUDE_API_KEY:
            client = anthropic.Anthropic(api_key=settings.CLAUDE_API_KEY)
            message = client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=1024,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            answer = message.content[0].text

        # Fallback на OpenAI
        elif openai_available and settings.OPENAI_API_KEY:
            client = OpenAI(api_key=settings.OPENAI_API_KEY)
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Ты - эксперт по строительным нормативам России."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1024
            )
            answer = response.choices[0].message.content

        else:
            # Заглушка если нет ИИ API
            answer = f"""
Это демо-ответ ИИ консультанта.

Для вопроса: "{request.question}"

Рекомендуем обратиться к следующим нормативам:
{regulations_context}

Для полноценной работы ИИ-консультанта необходимо настроить API ключи OpenAI или Claude.
"""

        return {
            "answer": answer,
            "referenced_regulations": [reg.code for reg in relevant_regulations],
            "confidence": 0.85
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error calling AI API: {str(e)}"
        )


@router.post("/search-semantic")
async def semantic_search_regulations(
    query: str = Query(..., description="Поисковый запрос"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Семантический поиск по нормативам
    TODO: Интеграция с Elasticsearch и векторным поиском
    """
    # Заглушка для семантического поиска
    # В продакшене здесь будет Elasticsearch с BERT embeddings

    results = db.query(Regulation).filter(
        (Regulation.title.ilike(f"%{query}%")) |
        (Regulation.description.ilike(f"%{query}%"))
    ).limit(10).all()

    return {
        "query": query,
        "results": [
            {
                "id": reg.id,
                "code": reg.code,
                "title": reg.title,
                "score": 0.9  # Заглушка для релевантности
            }
            for reg in results
        ]
    }
