# Архитектура приложения "ТехНадзор"

## Общая архитектура

```
┌─────────────────────────────────────────────────────────────┐
│                    Mobile Applications                       │
│         (React Native - iOS & Android)                       │
│                                                               │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │  Camera  │  │ Hidden   │  │   AI     │  │Projects  │   │
│  │  Module  │  │  Works   │  │Consultant│  │  Module  │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
│                                                               │
│  Redux Store │ WatermelonDB (Offline) │ React Navigation   │
└─────────────────────────────────────────────────────────────┘
                            │
                    HTTPS REST API
                            │
┌─────────────────────────────────────────────────────────────┐
│                     API Gateway (FastAPI)                    │
│                                                               │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              API v1 Endpoints                         │  │
│  │  /auth  /projects  /inspections  /regulations        │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ PostgreSQL  │    │   Redis     │    │Elasticsearch│
│  Database   │    │   Cache     │    │   Search    │
└─────────────┘    └─────────────┘    └─────────────┘
        │
        ▼
┌─────────────────────────────────────────────────────────────┐
│                    Background Workers                        │
│                      (Celery)                                │
│                                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ ML Inference │  │   Document   │  │     Email    │     │
│  │   (AI/ML)    │  │  Generation  │  │Notifications │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────────────────────────┐
│                  External Services                           │
│                                                               │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │   S3     │  │ OpenAI/  │  │  ГИСОГД  │  │   1С     │   │
│  │ Storage  │  │  Claude  │  │   API    │  │   API    │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
└─────────────────────────────────────────────────────────────┘
```

---

## Backend Архитектура (FastAPI)

### Структура директорий

```
backend/
├── alembic/                    # Миграции БД
│   ├── versions/
│   └── env.py
├── app/
│   ├── api/                    # API endpoints
│   │   └── v1/
│   │       ├── endpoints/
│   │       │   ├── auth.py
│   │       │   ├── projects.py
│   │       │   ├── inspections.py
│   │       │   ├── hidden_works.py
│   │       │   └── regulations.py
│   │       └── router.py
│   ├── models/                 # SQLAlchemy модели
│   │   ├── user.py
│   │   ├── project.py
│   │   ├── inspection.py
│   │   ├── hidden_works.py
│   │   ├── checklist.py
│   │   ├── document.py
│   │   ├── material.py
│   │   └── regulation.py
│   ├── schemas/                # Pydantic схемы
│   │   ├── user.py
│   │   ├── project.py
│   │   └── inspection.py
│   ├── services/               # Бизнес-логика
│   │   ├── ai_service.py
│   │   ├── ml_service.py
│   │   ├── storage_service.py
│   │   └── document_service.py
│   ├── core/                   # Ядро приложения
│   │   ├── security.py
│   │   └── dependencies.py
│   ├── config.py               # Конфигурация
│   ├── database.py             # Настройка БД
│   ├── main.py                 # Главный файл FastAPI
│   └── celery_app.py           # Celery приложение
├── tests/                      # Тесты
├── uploads/                    # Загруженные файлы
├── requirements.txt
├── Dockerfile
└── .env
```

### Слои архитектуры

1. **API Layer** (FastAPI endpoints)
   - Обработка HTTP запросов
   - Валидация входных данных (Pydantic)
   - Аутентификация и авторизация (JWT)

2. **Service Layer** (Бизнес-логика)
   - AI Service - работа с ИИ моделями
   - ML Service - распознавание дефектов
   - Storage Service - работа с S3
   - Document Service - генерация документов

3. **Data Layer** (SQLAlchemy ORM)
   - Модели базы данных
   - Миграции (Alembic)
   - Репозитории для доступа к данным

4. **Background Tasks** (Celery)
   - Асинхронная обработка фото
   - ML инференс
   - Генерация документов
   - Email уведомления

---

## Frontend Архитектура (React Native)

### Структура директорий

```
mobile/
├── src/
│   ├── screens/                # Экраны приложения
│   │   ├── auth/
│   │   │   ├── LoginScreen.tsx
│   │   │   └── RegisterScreen.tsx
│   │   ├── home/
│   │   │   └── HomeScreen.tsx
│   │   ├── projects/
│   │   │   ├── ProjectsScreen.tsx
│   │   │   └── ProjectDetailScreen.tsx
│   │   ├── inspections/
│   │   │   ├── CameraScreen.tsx
│   │   │   ├── InspectionScreen.tsx
│   │   │   └── PhotoGalleryScreen.tsx
│   │   ├── hiddenworks/
│   │   │   └── HiddenWorksScreen.tsx
│   │   └── ai/
│   │       └── AIConsultantScreen.tsx
│   ├── components/             # Переиспользуемые компоненты
│   │   ├── common/
│   │   │   ├── Button.tsx
│   │   │   ├── Input.tsx
│   │   │   └── Card.tsx
│   │   ├── camera/
│   │   │   └── CameraOverlay.tsx
│   │   └── chat/
│   │       └── MessageBubble.tsx
│   ├── navigation/             # Навигация
│   │   ├── RootNavigator.tsx
│   │   ├── AuthNavigator.tsx
│   │   └── MainNavigator.tsx
│   ├── store/                  # Redux
│   │   ├── store.ts
│   │   └── slices/
│   │       ├── authSlice.ts
│   │       ├── projectsSlice.ts
│   │       └── inspectionsSlice.ts
│   ├── services/               # API и сервисы
│   │   ├── api.ts
│   │   ├── camera.ts
│   │   ├── geolocation.ts
│   │   └── storage.ts
│   ├── utils/                  # Утилиты
│   │   ├── date.ts
│   │   ├── validation.ts
│   │   └── formatters.ts
│   ├── types/                  # TypeScript типы
│   │   ├── api.ts
│   │   └── models.ts
│   ├── config/                 # Конфигурация
│   │   └── api.ts
│   ├── theme/                  # Темы и стили
│   │   ├── colors.ts
│   │   ├── typography.ts
│   │   └── spacing.ts
│   └── assets/                 # Ассеты
│       ├── images/
│       ├── icons/
│       └── fonts/
├── android/                    # Android проект
├── ios/                        # iOS проект
├── app.json
├── package.json
└── tsconfig.json
```

### Архитектурные паттерны

1. **State Management** (Redux Toolkit)
   - Централизованное хранилище состояния
   - Redux slices для модулей
   - Redux Persist для офлайн режима

2. **Navigation** (React Navigation)
   - Stack Navigator для экранов
   - Tab Navigator для главной навигации
   - Deep linking support

3. **Offline First** (WatermelonDB)
   - Локальная база данных
   - Синхронизация с сервером
   - Работа без интернета

4. **Component Architecture**
   - Функциональные компоненты
   - React Hooks
   - TypeScript для типобезопасности

---

## База данных (PostgreSQL)

### ER Diagram

```
┌─────────────┐         ┌─────────────┐
│    users    │         │  projects   │
├─────────────┤         ├─────────────┤
│ id (PK)     │────────<│ created_by  │
│ email       │         │ name        │
│ full_name   │         │ address     │
│ role        │         │ status      │
└─────────────┘         └─────────────┘
                              │
                    ┌─────────┴─────────┐
                    │                   │
                    ▼                   ▼
            ┌─────────────┐     ┌─────────────┐
            │ inspections │     │hidden_works │
            ├─────────────┤     ├─────────────┤
            │ id (PK)     │     │ id (PK)     │
            │ project_id  │     │ project_id  │
            │ title       │     │ title       │
            │ status      │     │ status      │
            └─────────────┘     └─────────────┘
                    │                   │
                    ▼                   ▼
            ┌─────────────┐     ┌─────────────┐
            │inspection_  │     │hidden_work_ │
            │   photos    │     │    acts     │
            ├─────────────┤     ├─────────────┤
            │ id (PK)     │     │ id (PK)     │
            │inspection_id│     │ work_id     │
            │ file_url    │     │ act_number  │
            │ latitude    │     │ is_approved │
            │ longitude   │     └─────────────┘
            └─────────────┘
                    │
                    ▼
            ┌─────────────┐
            │   defect_   │
            │ detections  │
            ├─────────────┤
            │ id (PK)     │
            │ photo_id    │
            │ defect_type │
            │ severity    │
            └─────────────┘
```

### Основные таблицы

1. **users** - Пользователи системы
2. **projects** - Строительные объекты
3. **inspections** - Проверки
4. **inspection_photos** - Фотографии проверок
5. **defect_detections** - Обнаруженные дефекты
6. **hidden_works** - Скрытые работы
7. **hidden_work_acts** - Акты освидетельствования
8. **checklists** - Чек-листы
9. **checklist_items** - Пункты чек-листов
10. **documents** - Документы
11. **materials** - Материалы
12. **material_certificates** - Сертификаты материалов
13. **regulations** - Нормативы

---

## Безопасность

### Аутентификация
- JWT токены (Access + Refresh)
- Bcrypt для хеширования паролей
- OAuth2 Password Bearer

### Авторизация
- Role-based access control (RBAC)
- Проверка прав на уровне API

### Защита данных
- HTTPS для всех запросов
- Шифрование чувствительных данных
- Водяные знаки на фотографиях
- Audit log для критических операций

### Соответствие стандартам
- ГОСТ Р 57580 (защита данных)
- GDPR compliance (для международной версии)

---

## Масштабируемость

### Horizontal Scaling
- Stateless API (FastAPI)
- Load balancer (Nginx/Traefik)
- Replicated PostgreSQL
- Redis Cluster

### Vertical Scaling
- Optimized queries
- Database indexes
- Caching strategy
- CDN for static files

### Monitoring
- Prometheus metrics
- Grafana dashboards
- Sentry error tracking
- Logging (ELK stack)

---

## Развертывание

### Development
```bash
docker-compose up -d
```

### Production
```bash
# Kubernetes deployment
kubectl apply -f k8s/
```

### CI/CD
- GitHub Actions
- Automated testing
- Docker image building
- Deployment to staging/production

---

*Документ обновлен: 2025-11-07*
