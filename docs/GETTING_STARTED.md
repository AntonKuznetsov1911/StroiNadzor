# Руководство по запуску проекта "ТехНадзор"

## Быстрый старт

### Требования

#### Для Backend:
- Python 3.11+
- PostgreSQL 15+
- Redis 7+
- Docker & Docker Compose (опционально)

#### Для Mobile:
- Node.js 18+
- npm или yarn
- React Native CLI
- Xcode (для iOS)
- Android Studio (для Android)

---

## Backend Setup

### Вариант 1: С использованием Docker (рекомендуется)

```bash
# 1. Клонирование проекта (если нужно)
cd C:\Users\PC\StroiNadzor

# 2. Создание .env файла
cd backend
copy .env.example .env

# 3. Редактирование .env файла
# Откройте .env и измените необходимые параметры:
# - SECRET_KEY (сгенерируйте случайную строку)
# - OPENAI_API_KEY или CLAUDE_API_KEY (если есть)

# 4. Запуск всех сервисов через Docker
cd ..
docker-compose up -d

# 5. Проверка работы
# API будет доступен на http://localhost:8000
# Swagger документация: http://localhost:8000/docs
```

### Вариант 2: Локальная разработка

```bash
# 1. Создание виртуального окружения
cd backend
python -m venv venv

# Windows:
venv\Scripts\activate

# Linux/Mac:
source venv/bin/activate

# 2. Установка зависимостей
pip install -r requirements.txt

# 3. Настройка .env
copy .env.example .env
# Отредактируйте .env файл

# 4. Запуск PostgreSQL и Redis локально
# Убедитесь что PostgreSQL и Redis запущены

# 5. Создание базы данных
# Создайте БД "tehnadzor_db" в PostgreSQL

# 6. Применение миграций
alembic upgrade head

# 7. Запуск сервера
uvicorn app.main:app --reload

# API доступен на http://localhost:8000
```

### Создание первого пользователя

```bash
# Через API (Swagger UI)
# 1. Откройте http://localhost:8000/docs
# 2. Найдите POST /api/v1/auth/register
# 3. Создайте пользователя:
{
  "email": "admin@tehnadzor.ru",
  "password": "SecurePassword123!",
  "full_name": "Иван Петров",
  "position": "Старший инженер",
  "role": "engineer"
}
```

---

## Mobile App Setup

### Установка зависимостей

```bash
cd mobile

# Установка npm пакетов
npm install

# Для iOS (только на Mac):
cd ios
pod install
cd ..
```

### Конфигурация API

```typescript
// Отредактируйте src/config/api.ts
export const API_BASE_URL = 'http://YOUR_IP:8000/api/v1';
// Замените YOUR_IP на IP вашего компьютера в локальной сети
// Для Android эмулятора используйте: http://10.0.2.2:8000/api/v1
// Для iOS симулятора можно использовать: http://localhost:8000/api/v1
```

### Запуск на iOS

```bash
# Запуск Metro bundler
npm start

# В новом терминале:
npm run ios

# Или через Xcode:
# Откройте ios/TehNadzor.xcworkspace в Xcode и нажмите Run
```

### Запуск на Android

```bash
# Запуск Metro bundler
npm start

# В новом терминале:
npm run android

# Или через Android Studio:
# Откройте папку android/ в Android Studio и нажмите Run
```

---

## Разработка

### Backend

#### Создание новой миграции

```bash
cd backend
alembic revision --autogenerate -m "Описание изменений"
alembic upgrade head
```

#### Запуск тестов

```bash
pytest
```

#### Создание нового API endpoint

1. Создайте Pydantic схему в `app/schemas/`
2. Создайте endpoint в `app/api/v1/endpoints/`
3. Подключите роутер в `app/api/v1/router.py`

Пример:
```python
# app/api/v1/endpoints/example.py
from fastapi import APIRouter

router = APIRouter()

@router.get("/example")
async def get_example():
    return {"message": "Hello"}
```

### Mobile

#### Создание нового экрана

```typescript
// src/screens/ExampleScreen.tsx
import React from 'react';
import { View, Text } from 'react-native';

const ExampleScreen = () => {
  return (
    <View>
      <Text>Example Screen</Text>
    </View>
  );
};

export default ExampleScreen;
```

#### Добавление в навигацию

```typescript
// src/navigation/RootNavigator.tsx
<Stack.Screen name="Example" component={ExampleScreen} />
```

#### Работа с Redux

```typescript
// Использование в компоненте
import { useDispatch, useSelector } from 'react-redux';
import { fetchProjects } from '../store/slices/projectsSlice';

const MyComponent = () => {
  const dispatch = useDispatch();
  const { projects, loading } = useSelector((state) => state.projects);

  useEffect(() => {
    dispatch(fetchProjects());
  }, []);

  return <View>...</View>;
};
```

---

## Полезные команды

### Backend

```bash
# Форматирование кода
black app/

# Проверка типов
mypy app/

# Запуск Celery worker
celery -A app.celery_app worker --loglevel=info

# Очистка кэша Redis
redis-cli FLUSHALL
```

### Mobile

```bash
# Очистка кэша Metro
npm start -- --reset-cache

# Очистка сборки Android
cd android && ./gradlew clean && cd ..

# Очистка сборки iOS
cd ios && rm -rf build && pod install && cd ..

# Проверка кода
npm run lint

# Запуск тестов
npm test
```

---

## Troubleshooting

### Backend

**Проблема:** "alembic.util.exc.CommandError: Can't locate revision identified by..."

**Решение:**
```bash
# Удалите все миграции кроме базовой
rm backend/alembic/versions/*.py

# Создайте новую начальную миграцию
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

**Проблема:** "Connection refused to PostgreSQL"

**Решение:**
- Проверьте что PostgreSQL запущен
- Проверьте DATABASE_URL в .env
- Проверьте что база данных создана

### Mobile

**Проблема:** "Unable to resolve module..."

**Решение:**
```bash
# Очистите кэш и переустановите зависимости
rm -rf node_modules
npm install
npm start -- --reset-cache
```

**Проблема:** "Could not connect to development server"

**Решение:**
- Проверьте что Metro bundler запущен
- Проверьте что устройство/эмулятор в той же сети
- Для Android проверьте adb reverse:
```bash
adb reverse tcp:8081 tcp:8081
```

---

## Следующие шаги

### После успешного запуска:

1. **Тестовые данные**
   - Создайте несколько проектов через API
   - Загрузите базовые нормативы в БД
   - Создайте тестовые проверки

2. **Настройка ИИ**
   - Получите API ключи OpenAI или Claude
   - Добавьте их в .env
   - Протестируйте ИИ-консультанта

3. **Разработка**
   - Изучите структуру проекта
   - Прочитайте ARCHITECTURE.md
   - Ознакомьтесь с PROJECT_ROADMAP.md

4. **Deployment**
   - Настройте production окружение
   - Настройте CI/CD
   - Подготовьте к релизу в App Store/Google Play

---

## Документация API

После запуска backend, документация доступна по адресам:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

---

## Контакты и поддержка

- **GitHub:** [ссылка на репозиторий]
- **Email:** support@tehnadzor.ru
- **Документация:** https://docs.tehnadzor.ru

---

*Последнее обновление: 2025-11-07*
