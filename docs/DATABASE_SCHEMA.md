# Схема базы данных "ТехНадзор"

## Обзор

База данных PostgreSQL содержит 13 основных таблиц для хранения данных о пользователях, проектах, проверках, скрытых работах, нормативах и других сущностях.

---

## Таблицы

### 1. users - Пользователи

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(20) UNIQUE,
    full_name VARCHAR(255) NOT NULL,
    position VARCHAR(255),
    hashed_password VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL,  -- admin, engineer, supervisor, contractor, viewer

    avatar_url VARCHAR(500),
    company VARCHAR(255),
    certificates TEXT,  -- JSON

    is_active BOOLEAN DEFAULT TRUE,
    is_verified BOOLEAN DEFAULT FALSE,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP
);
```

**Индексы:**
- `idx_users_email` ON (email)
- `idx_users_role` ON (role)

---

### 2. projects - Проекты (объекты строительства)

```sql
CREATE TABLE projects (
    id SERIAL PRIMARY KEY,
    name VARCHAR(500) NOT NULL,
    description TEXT,
    project_type VARCHAR(50) NOT NULL,  -- residential, commercial, industrial, infrastructure, reconstruction
    status VARCHAR(50) DEFAULT 'planning',  -- planning, in_progress, on_hold, completed, cancelled

    address VARCHAR(500) NOT NULL,
    city VARCHAR(255),
    region VARCHAR(255),
    latitude FLOAT,
    longitude FLOAT,

    start_date TIMESTAMP,
    planned_end_date TIMESTAMP,
    actual_end_date TIMESTAMP,

    completion_percentage FLOAT DEFAULT 0.0,

    created_by INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Индексы:**
- `idx_projects_status` ON (status)
- `idx_projects_created_by` ON (created_by)
- `idx_projects_type` ON (project_type)

---

### 3. inspections - Проверки

```sql
CREATE TABLE inspections (
    id SERIAL PRIMARY KEY,
    project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    inspector_id INTEGER NOT NULL REFERENCES users(id),

    title VARCHAR(500) NOT NULL,
    description TEXT,
    status VARCHAR(50) DEFAULT 'draft',  -- draft, in_progress, completed, approved, rejected

    construction_phase VARCHAR(255),
    floor_level VARCHAR(50),
    section VARCHAR(100),

    latitude FLOAT,
    longitude FLOAT,

    inspection_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Индексы:**
- `idx_inspections_project` ON (project_id)
- `idx_inspections_inspector` ON (inspector_id)
- `idx_inspections_status` ON (status)
- `idx_inspections_date` ON (inspection_date)

---

### 4. inspection_photos - Фотографии проверок

```sql
CREATE TABLE inspection_photos (
    id SERIAL PRIMARY KEY,
    inspection_id INTEGER NOT NULL REFERENCES inspections(id) ON DELETE CASCADE,

    file_url VARCHAR(1000) NOT NULL,
    thumbnail_url VARCHAR(1000),
    file_size INTEGER,

    caption VARCHAR(500),
    latitude FLOAT,
    longitude FLOAT,
    taken_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    watermark_data TEXT,  -- JSON с метаданными водяного знака

    ai_analyzed BOOLEAN DEFAULT FALSE,
    ai_analysis_result TEXT,  -- JSON с результатами анализа

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Индексы:**
- `idx_photos_inspection` ON (inspection_id)
- `idx_photos_ai_analyzed` ON (ai_analyzed)

---

### 5. defect_detections - Обнаруженные дефекты

```sql
CREATE TABLE defect_detections (
    id SERIAL PRIMARY KEY,
    photo_id INTEGER NOT NULL REFERENCES inspection_photos(id) ON DELETE CASCADE,

    defect_type VARCHAR(50) NOT NULL,  -- crack, deviation, reinforcement, welding, waterproofing, concrete_quality, other
    severity VARCHAR(50) NOT NULL,  -- critical, major, minor, cosmetic

    description TEXT,
    recommendation TEXT,

    bbox_x FLOAT,
    bbox_y FLOAT,
    bbox_width FLOAT,
    bbox_height FLOAT,

    detected_by_ai BOOLEAN DEFAULT FALSE,
    confidence_score FLOAT,  -- 0.0 - 1.0

    is_fixed BOOLEAN DEFAULT FALSE,
    fixed_at TIMESTAMP,
    fix_verification_photo_url VARCHAR(1000),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Индексы:**
- `idx_defects_photo` ON (photo_id)
- `idx_defects_type` ON (defect_type)
- `idx_defects_severity` ON (severity)
- `idx_defects_fixed` ON (is_fixed)

---

### 6. hidden_works - Скрытые работы

```sql
CREATE TABLE hidden_works (
    id SERIAL PRIMARY KEY,
    project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,

    title VARCHAR(500) NOT NULL,
    description TEXT,
    work_type VARCHAR(50) NOT NULL,  -- foundation, reinforcement, waterproofing, utilities, electrical, ventilation, other
    status VARCHAR(50) DEFAULT 'pending',  -- pending, in_review, approved, rejected, closed

    floor_level VARCHAR(50),
    section VARCHAR(100),
    axis VARCHAR(100),

    planned_inspection_date TIMESTAMP,
    actual_inspection_date TIMESTAMP,
    closing_deadline TIMESTAMP,

    notification_sent BOOLEAN DEFAULT FALSE,
    notification_sent_at TIMESTAMP,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Индексы:**
- `idx_hidden_works_project` ON (project_id)
- `idx_hidden_works_status` ON (status)
- `idx_hidden_works_type` ON (work_type)

---

### 7. hidden_work_acts - Акты освидетельствования

```sql
CREATE TABLE hidden_work_acts (
    id SERIAL PRIMARY KEY,
    hidden_work_id INTEGER NOT NULL REFERENCES hidden_works(id) ON DELETE CASCADE,

    act_number VARCHAR(100) UNIQUE NOT NULL,
    act_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    inspector_id INTEGER NOT NULL REFERENCES users(id),
    contractor_representative VARCHAR(255),
    technical_supervision VARCHAR(255),

    is_approved BOOLEAN DEFAULT FALSE,
    comments TEXT,
    defects_found TEXT,  -- JSON

    photos TEXT,  -- JSON массив URL

    inspector_signature VARCHAR(1000),
    contractor_signature VARCHAR(1000),
    supervision_signature VARCHAR(1000),

    document_url VARCHAR(1000),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Индексы:**
- `idx_acts_work` ON (hidden_work_id)
- `idx_acts_number` ON (act_number)
- `idx_acts_approved` ON (is_approved)

---

### 8. checklist_templates - Шаблоны чек-листов

```sql
CREATE TABLE checklist_templates (
    id SERIAL PRIMARY KEY,

    name VARCHAR(500) NOT NULL,
    description TEXT,
    category VARCHAR(255),

    project_type VARCHAR(100),
    construction_phase VARCHAR(255),

    items_template TEXT NOT NULL,  -- JSON

    is_active BOOLEAN DEFAULT TRUE,
    is_default BOOLEAN DEFAULT FALSE,

    created_by INTEGER REFERENCES users(id),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

### 9. checklists - Чек-листы

```sql
CREATE TABLE checklists (
    id SERIAL PRIMARY KEY,
    project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    template_id INTEGER REFERENCES checklist_templates(id),
    inspector_id INTEGER NOT NULL REFERENCES users(id),

    name VARCHAR(500) NOT NULL,
    description TEXT,

    floor_level VARCHAR(50),
    section VARCHAR(100),

    total_items INTEGER DEFAULT 0,
    completed_items INTEGER DEFAULT 0,
    completion_percentage FLOAT DEFAULT 0.0,

    is_completed BOOLEAN DEFAULT FALSE,
    completed_at TIMESTAMP,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

### 10. checklist_items - Пункты чек-листов

```sql
CREATE TABLE checklist_items (
    id SERIAL PRIMARY KEY,
    checklist_id INTEGER NOT NULL REFERENCES checklists(id) ON DELETE CASCADE,

    title VARCHAR(500) NOT NULL,
    description TEXT,
    order_num INTEGER DEFAULT 0,

    is_required BOOLEAN DEFAULT FALSE,
    requires_photo BOOLEAN DEFAULT FALSE,
    regulation_reference VARCHAR(500),

    is_checked BOOLEAN DEFAULT FALSE,
    is_compliant BOOLEAN,
    checked_at TIMESTAMP,
    checked_by INTEGER REFERENCES users(id),

    comment TEXT,
    photo_urls TEXT,  -- JSON

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

### 11. documents - Документы

```sql
CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,

    title VARCHAR(500) NOT NULL,
    document_type VARCHAR(50) NOT NULL,  -- act, protocol, report, prescription, journal, executive, other
    document_number VARCHAR(100),

    file_url VARCHAR(1000) NOT NULL,
    file_name VARCHAR(500) NOT NULL,
    file_size INTEGER,
    mime_type VARCHAR(100),

    description TEXT,
    tags TEXT,  -- JSON

    created_by INTEGER NOT NULL REFERENCES users(id),
    document_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    version INTEGER DEFAULT 1,
    parent_document_id INTEGER REFERENCES documents(id),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

### 12. materials - Материалы

```sql
CREATE TABLE materials (
    id SERIAL PRIMARY KEY,
    project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,

    name VARCHAR(500) NOT NULL,
    category VARCHAR(255),
    manufacturer VARCHAR(255),
    supplier VARCHAR(255),

    batch_number VARCHAR(100),
    quantity FLOAT,
    unit VARCHAR(50),

    delivery_date TIMESTAMP,

    storage_location VARCHAR(255),
    storage_conditions TEXT,

    is_verified BOOLEAN DEFAULT FALSE,
    verified_by INTEGER REFERENCES users(id),
    verified_at TIMESTAMP,

    notes TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

### 13. material_certificates - Сертификаты материалов

```sql
CREATE TABLE material_certificates (
    id SERIAL PRIMARY KEY,
    material_id INTEGER NOT NULL REFERENCES materials(id) ON DELETE CASCADE,

    certificate_number VARCHAR(255) NOT NULL,
    certificate_type VARCHAR(100),
    issuer VARCHAR(255),
    issue_date TIMESTAMP,
    expiry_date TIMESTAMP,

    file_url VARCHAR(1000) NOT NULL,
    file_name VARCHAR(500) NOT NULL,

    ocr_extracted_data TEXT,  -- JSON

    is_verified BOOLEAN DEFAULT FALSE,
    verification_method VARCHAR(100),
    verification_result TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

### 14. regulations - Нормативы

```sql
CREATE TABLE regulations (
    id SERIAL PRIMARY KEY,

    code VARCHAR(100) UNIQUE NOT NULL,  -- СП 63.13330.2018
    title VARCHAR(1000) NOT NULL,
    full_name TEXT,

    regulation_type VARCHAR(50) NOT NULL,  -- СП, ГОСТ, СанПиН и т.д.

    description TEXT,
    content TEXT,

    is_active BOOLEAN DEFAULT TRUE,
    supersedes VARCHAR(100),
    superseded_by VARCHAR(100),

    publication_date TIMESTAMP,
    effective_date TIMESTAMP,

    keywords TEXT,  -- JSON
    categories TEXT,  -- JSON

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Индексы:**
- `idx_regulations_code` ON (code)
- `idx_regulations_type` ON (regulation_type)
- `idx_regulations_active` ON (is_active)

---

## Связи между таблицами

```
users (1) ──────┬──── (N) projects
                └──── (N) inspections

projects (1) ───┬──── (N) inspections
                ├──── (N) hidden_works
                ├──── (N) checklists
                ├──── (N) documents
                └──── (N) materials

inspections (1) ──── (N) inspection_photos

inspection_photos (1) ──── (N) defect_detections

hidden_works (1) ──── (N) hidden_work_acts

checklists (1) ──── (N) checklist_items

materials (1) ──── (N) material_certificates
```

---

## Создание базы данных

```sql
-- Создание базы данных
CREATE DATABASE tehnadzor_db
    WITH
    ENCODING = 'UTF8'
    LC_COLLATE = 'Russian_Russia.1251'
    LC_CTYPE = 'Russian_Russia.1251'
    TEMPLATE = template0;

-- Подключение к базе
\c tehnadzor_db

-- Создание расширений
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";  -- Для полнотекстового поиска
```

---

*Последнее обновление: 2025-11-07*
