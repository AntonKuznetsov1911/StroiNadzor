# Сводка компонентов мобильного приложения

## Созданные компоненты и модули

### 1. Общие компоненты (Common Components)

**Расположение:** `mobile/src/components/common/`

- **Button.tsx** - Универсальная кнопка
  - 5 вариантов: primary, secondary, danger, success, outline
  - 3 размера: small, medium, large
  - Поддержка состояния загрузки и disabled

- **Card.tsx** - Карточка-контейнер
  - Настраиваемый padding
  - Тень и скругленные углы

- **Input.tsx** - Текстовое поле ввода
  - Поддержка лейбла и обязательности
  - Отображение ошибок
  - Многострочный режим

- **LoadingScreen.tsx** - Экран загрузки
  - Полноэкранный индикатор
  - Настраиваемое сообщение

- **EmptyState.tsx** - Пустое состояние
  - Иконка, заголовок, описание
  - Опциональная кнопка действия

### 2. Компоненты форм (Form Components)

**Расположение:** `mobile/src/components/forms/`

- **DatePicker.tsx** - Выбор даты
  - Поддержка минимальной и максимальной даты
  - Отображение ошибок
  - Состояние disabled

- **Dropdown.tsx** - Выпадающий список
  - Поддержка поиска (опционально)
  - Множественный выбор
  - Модальное окно с опциями

- **Checkbox.tsx** - Чекбокс
  - Поддержка лейбла
  - Состояние disabled
  - Отображение ошибок

- **RadioButton.tsx** - Радио-кнопки
  - Вертикальное и горизонтальное расположение
  - Группировка опций
  - Отображение ошибок

### 3. Строительные компоненты (Construction Components)

**Расположение:** `mobile/src/components/construction/`

- **DefectCard.tsx** - Карточка дефекта
  - Отображение фото, типа дефекта
  - Индикатор серьезности (critical, major, minor, cosmetic)
  - Уровень уверенности ML-модели

- **InspectionCard.tsx** - Карточка проверки
  - Дата, время, местоположение
  - Результат проверки (passed, failed, with_remarks, pending)
  - Статистика (количество дефектов, фото)
  - Информация об инспекторе

- **StatusBadge.tsx** - Бейдж статуса
  - 5 типов: success, error, warning, info, default
  - 3 размера: small, medium, large

- **ProgressBar.tsx** - Прогресс-бар
  - Отображение процента выполнения
  - Настраиваемый цвет и высота
  - Опциональный лейбл

### 4. Утилиты (Utils)

**Расположение:** `mobile/src/utils/`

#### date.ts - Работа с датами
- `formatDate()` - Форматирование даты (ДД.ММ.ГГГГ)
- `formatDateTime()` - Дата и время
- `formatTime()` - Только время
- `getRelativeTime()` - Относительное время (2 часа назад)
- `isToday()` - Проверка, является ли дата сегодняшней
- `addDays()` - Добавление дней к дате

#### formatters.ts - Форматирование данных
- `formatPhone()` - Телефон в российском формате
- `formatCurrency()` - Валюта (руб.)
- `formatFileSize()` - Размер файла (КБ, МБ, ГБ)
- `truncateText()` - Обрезка текста с многоточием
- `formatPercentage()` - Процент
- `formatCoordinates()` - GPS координаты

#### validation.ts - Валидация
- `validateEmail()` - Email
- `validatePhone()` - Российский номер телефона
- `validatePassword()` - Пароль (минимум 8 символов, буквы и цифры)
- `validateRequired()` - Обязательное поле
- `validateMinLength()` - Минимальная длина
- `validateCoordinates()` - GPS координаты

#### permissions.ts - Разрешения
- `checkPermission()` - Проверка разрешения
- `requestPermission()` - Запрос разрешения
- `requestPermissionWithFallback()` - Запрос с диалогом настроек
- `requestMultiplePermissions()` - Множественный запрос
- Типы: camera, location, storage, microphone, notifications

#### camera.ts - Работа с камерой
- `checkCameraPermissions()` - Проверка разрешений
- `createPhotoMetadata()` - Создание метаданных фото (GPS, время, устройство)
- `validatePhoto()` - Валидация фото (размер, GPS)
- `compressPhoto()` - Сжатие фото
- `generatePhotoFileName()` - Генерация имени файла
- `calculateDistance()` - Расчет расстояния между координатами
- `isWithinProjectBounds()` - Проверка нахождения в пределах проекта

#### geolocation.ts - Геолокация
- `getCurrentLocation()` - Получение текущей геолокации
- `watchLocation()` - Наблюдение за изменением локации
- `isLocationEnabled()` - Проверка доступности GPS
- `requestLocationEnable()` - Запрос включения GPS
- `reverseGeocode()` - Получение адреса из координат
- `geocode()` - Получение координат из адреса
- `isAccuracyAcceptable()` - Проверка точности (до 50м)
- `getDirectionName()` - Название направления по углу

#### file.ts - Работа с файлами
- `getFileInfo()` - Информация о файле
- `fileExists()` - Проверка существования
- `deleteFile()` - Удаление
- `copyFile()` - Копирование
- `moveFile()` - Перемещение
- `readFileAsText()` - Чтение как текст
- `writeTextToFile()` - Запись текста
- `getFileExtension()` - Расширение файла
- `getMimeType()` - MIME тип
- `createDirectory()` - Создание директории
- `readDirectory()` - Список файлов
- `clearTemporaryFiles()` - Очистка временных файлов

#### network.ts - Работа с сетью
- `getNetworkState()` - Состояние сети
- `isConnected()` - Проверка подключения
- `isWifiConnected()` - Проверка WiFi
- `isCellularConnected()` - Проверка мобильной сети
- `isConnectionExpensive()` - Проверка платного трафика
- `subscribeToNetworkChanges()` - Подписка на изменения
- `pingServer()` - Проверка доступности сервера
- `measureDownloadSpeed()` - Измерение скорости
- `getConnectionQuality()` - Качество соединения
- `waitForConnection()` - Ожидание подключения
- `canDownloadLargeFiles()` - Можно ли загружать большие файлы
- `retryWithBackoff()` - Повтор с экспоненциальной задержкой

#### storage.ts - Локальное хранилище
- `setItem()` - Сохранение
- `getItem()` - Получение
- `removeItem()` - Удаление
- `clear()` - Очистка всего хранилища
- `multiGet()` - Множественное получение
- `multiSet()` - Множественное сохранение
- **Cache** класс - Кэш с TTL
  - `Cache.set()` - Сохранение с TTL
  - `Cache.get()` - Получение с проверкой TTL
  - `Cache.has()` - Проверка наличия
  - `Cache.clearExpired()` - Очистка устаревших
- **OfflineQueue** класс - Очередь офлайн-действий
  - `OfflineQueue.enqueue()` - Добавление в очередь
  - `OfflineQueue.getAll()` - Получение всей очереди
  - `OfflineQueue.remove()` - Удаление из очереди
  - `OfflineQueue.clear()` - Очистка очереди

### 5. Хуки (Hooks)

**Расположение:** `mobile/src/hooks/`

- **useDebounce.ts** - Debounce для отложенных обновлений
  - Использование: поиск, автосохранение

- **useKeyboard.ts** - Отслеживание клавиатуры
  - `isKeyboardVisible` - Видимость клавиатуры
  - `keyboardHeight` - Высота клавиатуры

- **useForm.ts** - Управление формами
  - Валидация
  - Отслеживание изменений
  - Обработка ошибок
  - Методы: `handleChange()`, `handleBlur()`, `handleSubmit()`, `reset()`

- **useLocation.ts** - Работа с геолокацией
  - Получение текущей локации
  - Наблюдение за изменениями
  - Обработка ошибок
  - `location`, `error`, `loading`, `refresh()`

- **useNetwork.ts** - Мониторинг сети
  - `isConnected` - Подключение к интернету
  - `networkType` - Тип сети (wifi, cellular)
  - `isConnectionExpensive` - Платный трафик
  - `refresh()` - Обновление состояния

- **useImagePicker.ts** - Выбор изображений
  - `pickFromGallery()` - Из галереи
  - `takePhoto()` - Съемка с камеры
  - `pickImage()` - Универсальный выбор
  - `loading` - Состояние загрузки

### 6. Тема (Theme)

**Расположение:** `mobile/src/theme/`

- **colors.ts** - Цветовая палитра
  - primary (синий), accent (зеленый)
  - success, error, warning, info
  - neutral (оттенки серого)

- **spacing.ts** - Отступы и размеры
  - xs: 4, sm: 8, md: 16, lg: 24, xl: 32, xxl: 48, xxxl: 64
  - borderRadius: sm, md, lg, full
  - iconSizes: sm, md, lg, xl

- **typography.ts** - Типографика
  - fontFamily: regular, medium, bold
  - fontSize: xs (12) → xxxl (32)
  - fontWeight: regular, medium, semibold, bold
  - lineHeight: tight, normal, relaxed

### 7. Константы (Constants)

**Расположение:** `mobile/src/constants/index.ts`

- **API** - Настройки API
  - `API_BASE_URL` - Базовый URL
  - `API_TIMEOUT` - Таймаут (30 сек)

- **Лимиты**
  - `MAX_PHOTO_SIZE_MB` - 10 МБ
  - `MAX_PHOTOS_PER_INSPECTION` - 50
  - `PHOTO_QUALITY` - 0.8
  - `LOCATION_ACCURACY_THRESHOLD` - 50м

- **Кэш**
  - `CACHE_TTL_SHORT` - 5 мин
  - `CACHE_TTL_MEDIUM` - 30 мин
  - `CACHE_TTL_LONG` - 24 часа

- **Роли, статусы, типы**
  - `USER_ROLES` - admin, engineer, supervisor, contractor, viewer
  - `PROJECT_STATUSES` - planning, in_progress, on_hold, completed, archived
  - `INSPECTION_RESULTS` - passed, failed, with_remarks, pending
  - `DEFECT_TYPES` - crack, deviation, reinforcement, welding, etc.
  - `DEFECT_SEVERITIES` - critical, major, minor, cosmetic

- **Сообщения**
  - `ERROR_MESSAGES` - Тексты ошибок
  - `SUCCESS_MESSAGES` - Сообщения об успехе

- **Маршруты**
  - `ROUTES` - Названия экранов для навигации

### 8. Типы TypeScript (Types)

**Расположение:** `mobile/src/types/index.ts`

Полный набор типов для:
- User, Project, Inspection, Photo
- Defect, HiddenWork, Checklist
- Document, Material, Regulation
- API запросы и ответы
- Redux State
- Навигация

## Структура проекта

```
mobile/
├── src/
│   ├── components/
│   │   ├── common/           # 5 компонентов
│   │   ├── forms/            # 4 компонента
│   │   ├── construction/     # 4 компонента
│   │   └── index.ts          # Экспорты
│   ├── utils/
│   │   ├── date.ts           # 6 функций
│   │   ├── formatters.ts     # 6 функций
│   │   ├── validation.ts     # 6 функций
│   │   ├── permissions.ts    # 4 функции
│   │   ├── camera.ts         # 10 функций
│   │   ├── geolocation.ts    # 8 функций
│   │   ├── file.ts           # 15 функций
│   │   ├── network.ts        # 13 функций
│   │   ├── storage.ts        # Cache + OfflineQueue
│   │   └── index.ts          # Экспорты
│   ├── hooks/
│   │   ├── useDebounce.ts
│   │   ├── useKeyboard.ts
│   │   ├── useForm.ts
│   │   ├── useLocation.ts
│   │   ├── useNetwork.ts
│   │   ├── useImagePicker.ts
│   │   └── index.ts          # Экспорты
│   ├── theme/
│   │   ├── colors.ts
│   │   ├── spacing.ts
│   │   └── typography.ts
│   ├── constants/
│   │   └── index.ts
│   └── types/
│       └── index.ts
```

## Итого создано:

- **Компоненты:** 13 (5 common + 4 forms + 4 construction)
- **Утилиты:** 9 модулей, 68+ функций
- **Хуки:** 6 кастомных хуков
- **Тема:** 3 модуля (цвета, отступы, типографика)
- **Константы:** 1 файл с 15+ группами констант
- **Типы:** 30+ TypeScript интерфейсов

## Примеры использования

### Компоненты

```typescript
import { Button, Card, Input } from '@/components';

<Card>
  <Input
    label="Email"
    value={email}
    onChange={setEmail}
    error={errors.email}
    required
  />
  <Button
    title="Войти"
    onPress={handleLogin}
    loading={loading}
    variant="primary"
  />
</Card>
```

### Утилиты

```typescript
import { formatDate, validateEmail, getCurrentLocation } from '@/utils';

const formattedDate = formatDate(new Date()); // 08.11.2025
const isValid = validateEmail('user@example.com'); // true
const location = await getCurrentLocation(); // { latitude, longitude }
```

### Хуки

```typescript
import { useForm, useLocation, useNetwork } from '@/hooks';

const { values, errors, handleChange, handleSubmit } = useForm({
  initialValues: { email: '', password: '' },
  validate: validateLoginForm,
  onSubmit: login,
});

const { location, loading } = useLocation({ watch: true });
const { isConnected, networkType } = useNetwork();
```

## Рекомендации по установке зависимостей

Для полной функциональности установите:

```bash
# Навигация
npm install @react-navigation/native @react-navigation/stack @react-navigation/bottom-tabs

# Redux
npm install @reduxjs/toolkit react-redux redux-persist

# Камера и изображения
npm install react-native-vision-camera react-native-image-picker react-native-image-resizer

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

## Готово к использованию

Все компоненты, утилиты и хуки готовы к использованию в мобильном приложении ТехНадзор. Код написан с учетом лучших практик TypeScript и React Native.
