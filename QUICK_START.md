# Быстрый старт - ТехНадзор

## Текущий статус

**Demo-сервер запущен и работает!**
- URL: http://localhost:8000
- Swagger UI: http://localhost:8000/docs
- HTML страница: C:\Users\PC\StroiNadzor\OPEN_IN_BROWSER.html

## 1. Просмотр API (прямо сейчас)

### Открыть Swagger UI
1. Откройте браузер
2. Перейдите: http://localhost:8000/docs
3. Доступные endpoints:
   - GET /api/v1/projects - Список проектов
   - GET /api/v1/inspections - Список проверок
   - GET /api/v1/hidden-works - Скрытые работы
   - POST /api/v1/regulations/ai-consult - AI консультант

### Тестирование API
```bash
# Получить список проектов
curl http://localhost:8000/api/v1/projects

# Получить список проверок
curl http://localhost:8000/api/v1/inspections

# AI консультация
curl -X POST http://localhost:8000/api/v1/regulations/ai-consult \
  -H "Content-Type: application/json" \
  -d "{\"question\":\"Какие требования к бетону М350?\"}"
```

## 2. Установка для полной разработки

### Backend

#### Требования
- Python 3.11+
- PostgreSQL 15 (опционально, для полной версии)
- Redis (опционально)

#### Установка зависимостей
```bash
cd C:\Users\PC\StroiNadzor\backend
pip install -r requirements.txt
```

#### Запуск demo-сервера (без БД)
```bash
# Уже запущен!
python demo_server.py
```

#### Запуск полного сервера (с БД)
```bash
# 1. Создать БД
createdb tehnadzor

# 2. Настроить .env
cp .env.example .env
# Отредактировать .env с настройками БД

# 3. Применить миграции
alembic upgrade head

# 4. Загрузить тестовые данные
python scripts/init_data.py

# 5. Запустить сервер
uvicorn app.main:app --reload --port 8000
```

### Mobile

#### Требования
- Node.js 18+
- npm или yarn
- React Native CLI
- Android Studio (для Android)
- Xcode (для iOS, только macOS)

#### Установка зависимостей
```bash
cd C:\Users\PC\StroiNadzor\mobile
npm install

# Или
yarn install
```

#### Установка необходимых библиотек
```bash
# Навигация
npm install @react-navigation/native @react-navigation/stack @react-navigation/bottom-tabs
npm install react-native-screens react-native-safe-area-context

# Redux
npm install @reduxjs/toolkit react-redux redux-persist

# Камера и изображения
npm install react-native-vision-camera
npm install react-native-image-picker
npm install react-native-image-resizer

# Геолокация
npm install @react-native-community/geolocation

# Сеть
npm install @react-native-community/netinfo

# Хранилище
npm install @react-native-async-storage/async-storage

# Файлы
npm install react-native-fs

# Разрешения
npm install react-native-permissions

# Утилиты
npm install react-native-device-info
```

#### Запуск приложения

**Android:**
```bash
# 1. Запустить Metro
npm start

# 2. Запустить на Android (в новом терминале)
npm run android
```

**iOS (только macOS):**
```bash
# 1. Установить pods
cd ios
pod install
cd ..

# 2. Запустить Metro
npm start

# 3. Запустить на iOS (в новом терминале)
npm run ios
```

## 3. Разработка с Docker

### Запуск всего стека
```bash
cd C:\Users\PC\StroiNadzor
docker-compose up -d
```

Это запустит:
- PostgreSQL на порту 5432
- Redis на порту 6379
- Elasticsearch на порту 9200
- MinIO на портах 9000, 9001
- Backend на порту 8000
- Celery worker

### Команды Docker
```bash
# Просмотр логов
docker-compose logs -f

# Остановка
docker-compose down

# Пересборка
docker-compose build

# Запуск конкретного сервиса
docker-compose up postgres redis
```

## 4. Работа с Makefile

Доступные команды:

```bash
# Запуск
make start          # Запустить все сервисы
make stop           # Остановить все сервисы
make restart        # Перезапустить

# Разработка
make dev            # Запуск в dev режиме
make logs           # Просмотр логов
make shell          # Войти в backend контейнер

# База данных
make migrate        # Применить миграции
make migrate-create # Создать новую миграцию
make seed           # Загрузить тестовые данные

# Тесты
make test           # Запустить все тесты
make test-backend   # Только backend тесты
make test-mobile    # Только mobile тесты

# Очистка
make clean          # Очистить временные файлы
make clean-all      # Полная очистка
```

## 5. Структура проекта

```
StroiNadzor/
├── backend/                    # Backend (FastAPI)
│   ├── app/
│   │   ├── api/               # API endpoints
│   │   ├── models/            # SQLAlchemy модели
│   │   ├── schemas/           # Pydantic схемы
│   │   ├── services/          # Бизнес-логика
│   │   ├── tasks/             # Celery задачи
│   │   └── utils/             # Утилиты
│   ├── tests/                 # Тесты
│   ├── demo_server.py         # Demo сервер ✓
│   └── requirements.txt
│
├── mobile/                     # Mobile (React Native)
│   ├── src/
│   │   ├── components/        # UI компоненты (13)
│   │   ├── screens/           # Экраны (13)
│   │   ├── services/          # API сервисы (5)
│   │   ├── store/             # Redux
│   │   ├── utils/             # Утилиты (9 модулей)
│   │   ├── hooks/             # Хуки (6)
│   │   ├── theme/             # Тема
│   │   ├── constants/         # Константы
│   │   └── types/             # TypeScript типы
│   └── package.json
│
├── docs/                       # Документация (9 файлов)
├── docker-compose.yml
├── Makefile
└── README.md
```

## 6. Тестирование

### Backend тесты
```bash
cd backend
pytest

# С покрытием
pytest --cov=app tests/

# Конкретный тест
pytest tests/test_auth.py
```

### Mobile тесты
```bash
cd mobile
npm test

# С покрытием
npm test -- --coverage

# Watch mode
npm test -- --watch
```

## 7. Полезные ссылки

### Локальные
- Backend API: http://localhost:8000
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- MinIO Console: http://localhost:9001
- Elasticsearch: http://localhost:9200

### Документация
- PROJECT_SUMMARY.md - Полная сводка
- ARCHITECTURE.md - Архитектура
- API_DOCUMENTATION.md - API документация
- MOBILE_COMPONENTS_SUMMARY.md - Компоненты мобильного приложения
- DEVELOPMENT_SUMMARY.md - Сводка разработки

## 8. Примеры использования

### Backend API

```python
import requests

# Регистрация
response = requests.post('http://localhost:8000/api/v1/auth/register', json={
    'email': 'engineer@example.com',
    'password': 'SecurePass123',
    'full_name': 'Иванов Иван',
    'role': 'engineer'
})

# Логин
response = requests.post('http://localhost:8000/api/v1/auth/login', data={
    'username': 'engineer@example.com',
    'password': 'SecurePass123'
})
token = response.json()['access_token']

# Получение проектов
headers = {'Authorization': f'Bearer {token}'}
response = requests.get('http://localhost:8000/api/v1/projects', headers=headers)
projects = response.json()
```

### Mobile компоненты

```typescript
import { Button, Card, Input } from '@/components';
import { useForm, useLocation, useNetwork } from '@/hooks';

function MyScreen() {
  const { values, errors, handleChange, handleSubmit } = useForm({
    initialValues: { name: '', description: '' },
    onSubmit: async (values) => {
      await createProject(values);
    }
  });

  const { location } = useLocation();
  const { isConnected } = useNetwork();

  return (
    <Card>
      <Input
        label="Название"
        value={values.name}
        onChange={(value) => handleChange('name', value)}
        error={errors.name}
        required
      />

      <Button
        title="Создать"
        onPress={handleSubmit}
        disabled={!isConnected}
      />
    </Card>
  );
}
```

## 9. Решение проблем

### Backend не запускается
```bash
# Проверить Python версию
python --version  # Должно быть 3.11+

# Переустановить зависимости
pip install --upgrade -r requirements.txt

# Запустить demo-сервер (без БД)
python demo_server.py
```

### Mobile не запускается
```bash
# Очистить кэш
cd mobile
npm start -- --reset-cache

# Переустановить node_modules
rm -rf node_modules
npm install

# Android - очистить build
cd android
./gradlew clean
cd ..
```

### Порт 8000 занят
```bash
# Windows - найти процесс
netstat -ano | findstr :8000

# Убить процесс
taskkill /PID <PID> /F

# Или запустить на другом порту
python demo_server.py --port 8001
```

## 10. Следующие шаги

1. **Ознакомиться с документацией**
   - Прочитать PROJECT_SUMMARY.md
   - Изучить ARCHITECTURE.md
   - Посмотреть примеры в API_DOCUMENTATION.md

2. **Настроить окружение**
   - Установить все зависимости
   - Настроить IDE (VS Code, PyCharm)
   - Установить расширения

3. **Запустить проект**
   - Backend demo-сервер (уже работает!)
   - Mobile приложение
   - Протестировать API

4. **Начать разработку**
   - Выбрать задачу из PROJECT_ROADMAP.md
   - Создать ветку в git
   - Реализовать функционал
   - Написать тесты
   - Создать PR

---

**Нужна помощь?**
- Проверьте документацию в папке `docs/`
- Изучите примеры в `backend/demo_server.py`
- Посмотрите компоненты в `mobile/src/`

**Удачной разработки! 🚀**
