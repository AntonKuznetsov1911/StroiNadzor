# API Endpoints - ТехНадзор

**Демо-сервер:** http://localhost:8000
**Swagger UI:** http://localhost:8000/docs
**ReDoc:** http://localhost:8000/redoc

---

## Аутентификация

### `GET /api/v1/auth/me`
Получение информации о текущем пользователе

**Response:**
```json
{
  "id": 1,
  "email": "engineer@tehnadzor.ru",
  "full_name": "Иван Петров",
  "role": "engineer",
  "position": "Старший инженер"
}
```

---

## Проекты

### `GET /api/v1/projects`
Получение списка всех проектов

**Response:**
```json
[
  {
    "id": 1,
    "name": "ЖК 'Новый горизонт'",
    "address": "г. Москва, Ленинский проспект, д. 123",
    "status": "in_progress",
    "completion_percentage": 68.0,
    "description": "Жилой комплекс на 500 квартир"
  }
]
```

### `GET /api/v1/projects/{project_id}`
Получение проекта по ID

**Parameters:**
- `project_id` (path) - ID проекта

---

## Проверки

### `GET /api/v1/inspections`
Получение списка всех проверок

**Response:**
```json
[
  {
    "id": 1,
    "project_id": 1,
    "title": "Проверка качества бетона",
    "status": "completed",
    "inspection_date": "2025-11-08T10:30:00"
  }
]
```

### `GET /api/v1/inspections/{inspection_id}`
Получение проверки по ID

---

## Скрытые работы

### `GET /api/v1/hidden-works`
Получение списка скрытых работ

**Response:**
```json
[
  {
    "id": 1,
    "project_id": 1,
    "title": "Армирование фундамента",
    "work_type": "reinforcement",
    "status": "pending"
  }
]
```

---

## Нормативы

### `GET /api/v1/regulations`
Получение списка нормативных документов

**Response:**
```json
[
  {
    "id": 1,
    "code": "СП 63.13330.2018",
    "title": "Бетонные и железобетонные конструкции",
    "regulation_type": "СП"
  }
]
```

### `POST /api/v1/regulations/ai-consult`
ИИ-консультант по нормативам

**Request:**
```json
{
  "question": "Какая минимальная толщина защитного слоя бетона?",
  "context": "Работа на 5 этаже"
}
```

**Response:**
```json
{
  "answer": "Демо-ответ с рекомендациями...",
  "referenced_regulations": ["СП 63.13330.2018", "СП 70.13330.2012"],
  "confidence": 0.85
}
```

---

## Статистика

### `GET /api/v1/stats`
Базовая статистика

**Response:**
```json
{
  "total_projects": 2,
  "total_inspections": 2,
  "total_hidden_works": 2,
  "total_regulations": 3,
  "active_users": 2
}
```

### `GET /api/v1/statistics/dashboard`
Полная статистика для дашборда

**Response:**
```json
{
  "summary": {
    "total_projects": 2,
    "active_projects": 2,
    "total_inspections": 2,
    "recent_inspections": 2,
    "total_defects": 2,
    "critical_defects": 1,
    "pending_hidden_works": 1
  },
  "projects_by_status": {
    "in_progress": 2,
    "planning": 0,
    "completed": 0
  },
  "inspections_by_result": {
    "completed": 1,
    "in_progress": 1
  }
}
```

### `GET /api/v1/statistics/project/{project_id}`
Статистика по конкретному проекту

**Response:**
```json
{
  "project_id": 1,
  "project_name": "ЖК 'Новый горизонт'",
  "completion_percentage": 68.0,
  "inspections": {
    "total": 2,
    "by_result": {
      "completed": 1,
      "in_progress": 1
    }
  },
  "photos": {
    "total": 2,
    "with_defects": 1
  },
  "defects": {
    "by_type": {
      "crack": 1,
      "deviation": 1
    },
    "by_severity": {
      "critical": 1,
      "minor": 1
    }
  },
  "hidden_works": {
    "by_status": {
      "pending": 1,
      "approved": 1
    }
  }
}
```

### `GET /api/v1/statistics/trends`
Тренды за период

**Parameters:**
- `days` (query, default=30) - Количество дней

**Response:**
```json
{
  "period_days": 30,
  "inspections_trend": [
    {"date": "2025-11-08", "count": 3},
    {"date": "2025-11-07", "count": 2}
  ],
  "defects_trend": [
    {"date": "2025-11-08", "count": 1},
    {"date": "2025-11-07", "count": 0}
  ]
}
```

---

## Поиск

### `GET /api/v1/search/global`
Глобальный поиск по всем сущностям

**Parameters:**
- `q` (query, required, min_length=2) - Поисковый запрос

**Response:**
```json
{
  "query": "горизонт",
  "results": {
    "projects": [
      {
        "id": 1,
        "name": "ЖК 'Новый горизонт'",
        "type": "project",
        "description": "Жилой комплекс на 500 квартир"
      }
    ],
    "inspections": [],
    "hidden_works": [],
    "documents": []
  },
  "total_results": 1
}
```

### `GET /api/v1/search/projects`
Расширенный поиск по проектам

**Parameters:**
- `q` (query, required, min_length=2) - Поисковый запрос
- `status` (query, optional) - Фильтр по статусу

**Response:**
```json
{
  "query": "москва",
  "filters": {
    "status": "in_progress"
  },
  "results": [
    {
      "id": 1,
      "name": "ЖК 'Новый горизонт'",
      "description": "Жилой комплекс на 500 квартир",
      "status": "in_progress",
      "address": "г. Москва, Ленинский проспект, д. 123"
    }
  ],
  "count": 1
}
```

### `GET /api/v1/search/regulations`
Поиск по нормативным документам

**Parameters:**
- `q` (query, required, min_length=2) - Поиск по коду/названию

**Response:**
```json
{
  "query": "бетон",
  "results": [
    {
      "id": 1,
      "code": "СП 63.13330.2018",
      "title": "Бетонные и железобетонные конструкции",
      "regulation_type": "СП"
    }
  ],
  "count": 1
}
```

### `GET /api/v1/search/autocomplete`
Автодополнение для поиска

**Parameters:**
- `q` (query, required, min_length=1) - Начало текста
- `entity_type` (query, default="all") - Тип сущности (all/projects/inspections/documents)
- `limit` (query, default=10, max=20) - Лимит результатов

**Response:**
```json
{
  "query": "жк",
  "suggestions": [
    {"text": "ЖК 'Новый горизонт'", "type": "project"}
  ]
}
```

---

## Экспорт данных

### `GET /api/v1/export/projects/csv`
Экспорт всех проектов в CSV

**Response:** Файл CSV с проектами
- Заголовки: ID, Название, Статус, Адрес, Прогресс %
- Content-Type: text/csv
- Имя файла: projects_YYYYMMDD_HHMMSS.csv

### `GET /api/v1/export/inspections/csv`
Экспорт проверок в CSV

**Parameters:**
- `project_id` (query, optional) - Фильтр по проекту

**Response:** Файл CSV с проверками
- Заголовки: ID, Проект ID, Название, Статус, Дата
- Content-Type: text/csv
- Имя файла: inspections_YYYYMMDD_HHMMSS.csv

### `GET /api/v1/export/project/{project_id}/json`
Полный экспорт проекта со всеми данными в JSON

**Parameters:**
- `project_id` (path) - ID проекта

**Response:** Файл JSON
```json
{
  "project": {...},
  "inspections": [...],
  "hidden_works": [...],
  "export_date": "2025-11-08T10:30:00",
  "exported_by": "Demo User"
}
```

### `POST /api/v1/export/batch-export`
Пакетный экспорт нескольких проектов

**Request:**
```json
{
  "project_ids": [1, 2],
  "format": "json"
}
```

**Response:** Файл JSON с массивом проектов
- Content-Type: application/json
- Имя файла: batch_export_YYYYMMDD_HHMMSS.json

---

## Служебные endpoints

### `GET /`
Информация о сервере

**Response:**
```json
{
  "message": "ТехНадзор API (Demo)",
  "version": "1.0.0",
  "status": "running",
  "docs": "/docs",
  "note": "Это демо-версия без подключения к базе данных"
}
```

### `GET /health`
Health check

**Response:**
```json
{
  "status": "healthy",
  "service": "tehnadzor-api-demo"
}
```

---

## Общее количество endpoints

- **Аутентификация:** 1 endpoint
- **Проекты:** 2 endpoints
- **Проверки:** 2 endpoints
- **Скрытые работы:** 1 endpoint
- **Нормативы:** 2 endpoints
- **Статистика:** 4 endpoints
- **Поиск:** 4 endpoints
- **Экспорт:** 4 endpoints
- **Служебные:** 2 endpoints

**ИТОГО: 22 endpoints** ✅

---

## Примеры использования

### Curl примеры

**Получить список проектов:**
```bash
curl http://localhost:8000/api/v1/projects
```

**Глобальный поиск:**
```bash
curl "http://localhost:8000/api/v1/search/global?q=бетон"
```

**Экспорт проектов в CSV:**
```bash
curl http://localhost:8000/api/v1/export/projects/csv -o projects.csv
```

**ИИ-консультант:**
```bash
curl -X POST http://localhost:8000/api/v1/regulations/ai-consult \
  -H "Content-Type: application/json" \
  -d '{"question":"Минимальная толщина бетона?"}'
```

**Статистика дашборда:**
```bash
curl http://localhost:8000/api/v1/statistics/dashboard
```

**Автодополнение:**
```bash
curl "http://localhost:8000/api/v1/search/autocomplete?q=жк&entity_type=projects"
```

---

## Примечания

- Все endpoints работают с демо-данными (без реальной БД)
- Для полной версии с PostgreSQL используйте docker-compose
- Swagger UI доступен по адресу http://localhost:8000/docs
- Все ответы в формате JSON (кроме CSV/JSON экспорта)
- Поддержка CORS для всех origins (настроено в middleware)

---

**Дата создания:** 08.11.2025
**Версия:** 1.0.0 (Demo)
**Статус:** ✅ Работает на http://localhost:8000
