# API Документация "ТехНадзор"

## Базовый URL

```
Development: http://localhost:8000/api/v1
Production: https://api.tehnadzor.ru/api/v1
```

## Аутентификация

Все защищенные эндпоинты требуют JWT токен в заголовке:

```
Authorization: Bearer <access_token>
```

---

## Эндпоинты

### 1. Аутентификация

#### POST /auth/register
Регистрация нового пользователя.

**Request:**
```json
{
  "email": "user@example.com",
  "password": "SecurePass123!",
  "full_name": "Иван Иванов",
  "phone": "+7 (999) 123-45-67",
  "position": "Старший инженер",
  "company": "СтройКонтроль",
  "role": "engineer"
}
```

**Response (201):**
```json
{
  "id": 1,
  "email": "user@example.com",
  "full_name": "Иван Иванов",
  "role": "engineer",
  "is_active": true,
  "created_at": "2025-11-07T10:00:00Z"
}
```

#### POST /auth/login
Вход в систему.

**Request (form-data):**
```
username: user@example.com
password: SecurePass123!
```

**Response (200):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "full_name": "Иван Иванов",
    "role": "engineer"
  }
}
```

#### GET /auth/me
Получение информации о текущем пользователе.

**Headers:**
```
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "id": 1,
  "email": "user@example.com",
  "full_name": "Иван Иванов",
  "position": "Старший инженер",
  "role": "engineer",
  "company": "СтройКонтроль"
}
```

---

### 2. Проекты

#### GET /projects
Получение списка проектов.

**Query Parameters:**
- `skip` (int): Пропустить записи (default: 0)
- `limit` (int): Количество записей (default: 20, max: 100)

**Response (200):**
```json
{
  "projects": [
    {
      "id": 1,
      "name": "ЖК 'Новый горизонт'",
      "address": "г. Москва, Ленинский проспект, д. 123",
      "status": "in_progress",
      "completion_percentage": 68.0,
      "created_at": "2025-05-01T10:00:00Z"
    }
  ],
  "total": 1,
  "page": 1,
  "page_size": 20
}
```

#### GET /projects/{project_id}
Получение деталей проекта.

**Response (200):**
```json
{
  "id": 1,
  "name": "ЖК 'Новый горизонт'",
  "description": "Жилой комплекс на 500 квартир",
  "project_type": "residential",
  "status": "in_progress",
  "address": "г. Москва, Ленинский проспект, д. 123",
  "completion_percentage": 68.0,
  "start_date": "2025-05-01T00:00:00Z",
  "planned_end_date": "2026-11-01T00:00:00Z"
}
```

#### POST /projects
Создание нового проекта.

**Request:**
```json
{
  "name": "ЖК 'Новый горизонт'",
  "description": "Жилой комплекс на 500 квартир",
  "project_type": "residential",
  "address": "г. Москва, Ленинский проспект, д. 123",
  "city": "Москва",
  "latitude": 55.751244,
  "longitude": 37.618423
}
```

**Response (201):**
```json
{
  "id": 1,
  "name": "ЖК 'Новый горизонт'",
  "status": "planning",
  "completion_percentage": 0.0,
  "created_by": 1,
  "created_at": "2025-11-07T10:00:00Z"
}
```

#### PATCH /projects/{project_id}
Обновление проекта.

**Request:**
```json
{
  "status": "in_progress",
  "completion_percentage": 50.0
}
```

---

### 3. Проверки (Inspections)

#### POST /inspections
Создание новой проверки.

**Request:**
```json
{
  "project_id": 1,
  "title": "Проверка качества бетона",
  "description": "Осмотр монолитных конструкций 5 этажа",
  "construction_phase": "Монолитные работы",
  "floor_level": "5",
  "latitude": 55.751244,
  "longitude": 37.618423
}
```

**Response (201):**
```json
{
  "id": 1,
  "project_id": 1,
  "inspector_id": 1,
  "title": "Проверка качества бетона",
  "status": "draft",
  "created_at": "2025-11-07T10:00:00Z"
}
```

#### GET /inspections/{inspection_id}
Получение проверки с фотографиями.

**Response (200):**
```json
{
  "id": 1,
  "title": "Проверка качества бетона",
  "status": "completed",
  "photos": [
    {
      "id": 1,
      "file_url": "/uploads/inspections/1/photo1.jpg",
      "caption": "Трещина в бетоне",
      "latitude": 55.751244,
      "longitude": 37.618423,
      "taken_at": "2025-11-07T10:00:00Z",
      "ai_analyzed": true
    }
  ]
}
```

#### POST /inspections/{inspection_id}/photos
Загрузка фотографии для проверки.

**Request (multipart/form-data):**
```
file: <binary>
caption: "Трещина в бетоне"
latitude: 55.751244
longitude: 37.618423
```

**Response (200):**
```json
{
  "id": 1,
  "inspection_id": 1,
  "file_url": "/uploads/inspections/1/photo1.jpg",
  "latitude": 55.751244,
  "longitude": 37.618423,
  "taken_at": "2025-11-07T10:00:00Z"
}
```

#### POST /inspections/{inspection_id}/analyze
Запуск ИИ анализа фотографий проверки.

**Response (200):**
```json
{
  "inspection_id": 1,
  "status": "analyzing",
  "message": "AI analysis started"
}
```

---

### 4. Скрытые работы

#### GET /hidden-works
Получение списка скрытых работ.

**Query Parameters:**
- `project_id` (int): Фильтр по проекту
- `status` (string): Фильтр по статусу

**Response (200):**
```json
[
  {
    "id": 1,
    "project_id": 1,
    "title": "Армирование фундамента",
    "work_type": "reinforcement",
    "status": "pending",
    "floor_level": "Фундамент",
    "planned_inspection_date": "2025-11-10T10:00:00Z"
  }
]
```

#### POST /hidden-works
Создание записи о скрытых работах.

**Request:**
```json
{
  "project_id": 1,
  "title": "Армирование фундамента",
  "description": "Укладка арматурного каркаса",
  "work_type": "reinforcement",
  "floor_level": "Фундамент",
  "planned_inspection_date": "2025-11-10T10:00:00Z"
}
```

#### POST /hidden-works/{work_id}/acts
Создание акта освидетельствования.

**Request:**
```json
{
  "act_number": "АКТ-001-2025",
  "contractor_representative": "Иванов И.И.",
  "is_approved": true,
  "comments": "Работы выполнены согласно проекту"
}
```

**Response (201):**
```json
{
  "id": 1,
  "hidden_work_id": 1,
  "act_number": "АКТ-001-2025",
  "is_approved": true,
  "document_url": "/uploads/acts/act_001_2025.pdf",
  "created_at": "2025-11-07T10:00:00Z"
}
```

---

### 5. Нормативы и ИИ-консультант

#### GET /regulations
Получение списка нормативов.

**Query Parameters:**
- `search` (string): Поиск по коду или названию
- `regulation_type` (string): Фильтр по типу (СП, ГОСТ и т.д.)
- `skip` (int): Пропустить записи
- `limit` (int): Количество записей

**Response (200):**
```json
[
  {
    "id": 1,
    "code": "СП 63.13330.2018",
    "title": "Бетонные и железобетонные конструкции",
    "regulation_type": "СП",
    "is_active": true
  }
]
```

#### POST /regulations/ai-consult
Запрос к ИИ-консультанту.

**Request:**
```json
{
  "question": "Какие требования к защитному слою бетона для арматуры?",
  "context": "Жилое здание, монолитные конструкции"
}
```

**Response (200):**
```json
{
  "answer": "Согласно СП 63.13330.2018, минимальный защитный слой бетона для арматуры...",
  "referenced_regulations": ["СП 63.13330.2018", "СП 28.13330.2017"],
  "confidence": 0.92
}
```

---

## Коды ошибок

| Код | Описание |
|-----|----------|
| 400 | Bad Request - Неверные параметры запроса |
| 401 | Unauthorized - Не авторизован |
| 403 | Forbidden - Нет доступа |
| 404 | Not Found - Ресурс не найден |
| 422 | Unprocessable Entity - Ошибка валидации |
| 500 | Internal Server Error - Внутренняя ошибка сервера |

---

## Rate Limiting

- Аутентифицированные пользователи: 1000 запросов/час
- Неаутентифицированные: 100 запросов/час

---

## Websocket (для чата и уведомлений)

```
ws://localhost:8000/ws/{user_id}
```

Будет реализовано в v1.0

---

*Документ обновлен: 2025-11-07*
