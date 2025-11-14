# Production Deployment Guide - ТехНадзор

**Дата:** 08.11.2025
**Версия:** 1.2.0

---

## 📋 Предварительные требования

### Системные требования
- **OS:** Ubuntu 20.04+ / CentOS 8+ / Debian 11+
- **CPU:** 4+ cores
- **RAM:** 8+ GB
- **Disk:** 100+ GB SSD
- **Docker:** 20.10+
- **Docker Compose:** 2.0+

### Домен и SSL
- Зарегистрированный домен (например, tehnadzor.ru)
- SSL сертификат (Let's Encrypt или коммерческий)

---

## 🚀 Шаг 1: Подготовка сервера

### 1.1 Установка Docker

```bash
# Обновление системы
sudo apt update && sudo apt upgrade -y

# Установка Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Добавление пользователя в группу docker
sudo usermod -aG docker $USER

# Установка Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Проверка
docker --version
docker-compose --version
```

### 1.2 Настройка firewall

```bash
# UFW firewall
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw enable
```

---

## 🔧 Шаг 2: Настройка проекта

### 2.1 Клонирование репозитория

```bash
git clone https://github.com/your-org/StroiNadzor.git
cd StroiNadzor
```

### 2.2 Создание .env файла

```bash
cp .env.example .env
nano .env
```

**Важные переменные для production:**

```env
# Database
POSTGRES_PASSWORD=STRONG_PASSWORD_HERE
DATABASE_URL=postgresql://postgres:STRONG_PASSWORD_HERE@postgres:5432/tehnadzor

# Security
SECRET_KEY=GENERATE_RANDOM_64_CHAR_STRING
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# MinIO
MINIO_ROOT_PASSWORD=STRONG_MINIO_PASSWORD

# AI APIs
OPENAI_API_KEY=sk-your-real-openai-key
CLAUDE_API_KEY=your-real-claude-key

# Email
SMTP_HOST=smtp.gmail.com
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# Environment
ENVIRONMENT=production
DEBUG=false

# CORS
ALLOWED_ORIGINS=https://tehnadzor.ru,https://app.tehnadzor.ru
```

### 2.3 Генерация SECRET_KEY

```bash
python3 -c "import secrets; print(secrets.token_urlsafe(64))"
```

---

## 🐳 Шаг 3: Развертывание с Docker Compose

### 3.1 Сборка и запуск

```bash
# Сборка образов
docker-compose -f docker-compose.prod.yml build

# Запуск сервисов
docker-compose -f docker-compose.prod.yml up -d

# Проверка статуса
docker-compose -f docker-compose.prod.yml ps
```

### 3.2 Применение миграций

```bash
# Подождать пока БД запустится (10-15 секунд)
sleep 15

# Применить миграции
docker-compose -f docker-compose.prod.yml exec backend alembic upgrade head

# Заполнить начальными данными (опционально)
docker-compose -f docker-compose.prod.yml exec backend python scripts/seed_data.py
```

### 3.3 Создание superuser

```bash
docker-compose -f docker-compose.prod.yml exec backend python scripts/create_superuser.py
```

---

## 🔒 Шаг 4: SSL сертификат (Let's Encrypt)

### 4.1 Установка Certbot

```bash
sudo apt install certbot python3-certbot-nginx -y
```

### 4.2 Получение сертификата

```bash
# Остановить nginx если запущен
docker-compose -f docker-compose.prod.yml stop nginx

# Получить сертификат
sudo certbot certonly --standalone -d tehnadzor.ru -d www.tehnadzor.ru

# Копировать сертификаты
sudo cp /etc/letsencrypt/live/tehnadzor.ru/fullchain.pem ./nginx/ssl/
sudo cp /etc/letsencrypt/live/tehnadzor.ru/privkey.pem ./nginx/ssl/

# Установить права
sudo chmod 644 ./nginx/ssl/*.pem

# Запустить nginx
docker-compose -f docker-compose.prod.yml up -d nginx
```

### 4.3 Auto-renewal

```bash
# Добавить cron job для авто-обновления
sudo crontab -e

# Добавить строку:
0 0 1 * * certbot renew --quiet && docker-compose -f /path/to/StroiNadzor/docker-compose.prod.yml restart nginx
```

---

## 📊 Шаг 5: Мониторинг

### 5.1 Проверка health

```bash
# Использовать Makefile
make health

# Или вручную
curl https://tehnadzor.ru/health
```

### 5.2 Просмотр логов

```bash
# Все логи
docker-compose -f docker-compose.prod.yml logs -f

# Только backend
docker-compose -f docker-compose.prod.yml logs -f backend

# Только Celery
docker-compose -f docker-compose.prod.yml logs -f celery_worker
```

### 5.3 Настройка Sentry (опционально)

```bash
# Добавить в .env
SENTRY_DSN=https://your-sentry-dsn

# Перезапустить backend
docker-compose -f docker-compose.prod.yml restart backend
```

---

## 💾 Шаг 6: Backup

### 6.1 Автоматический backup БД

```bash
# Создать скрипт backup
cat > /usr/local/bin/backup-tehnadzor.sh << 'EOF'
#!/bin/bash
BACKUP_DIR=/backups/tehnadzor
DATE=$(date +%Y%m%d_%H%M%S)
mkdir -p $BACKUP_DIR
docker exec tehnadzor_postgres pg_dump -U postgres tehnadzor | gzip > $BACKUP_DIR/db_backup_$DATE.sql.gz
find $BACKUP_DIR -name "db_backup_*.sql.gz" -mtime +7 -delete
EOF

chmod +x /usr/local/bin/backup-tehnadzor.sh

# Добавить в cron (каждый день в 2:00)
sudo crontab -e
# Добавить:
0 2 * * * /usr/local/bin/backup-tehnadzor.sh
```

### 6.2 Восстановление из backup

```bash
# Восстановить БД
gunzip < /backups/tehnadzor/db_backup_20251108_020000.sql.gz | \
docker exec -i tehnadzor_postgres psql -U postgres tehnadzor
```

---

## 🔄 Шаг 7: Обновление

### 7.1 Zero-downtime deployment

```bash
# Получить обновления
git pull origin main

# Собрать новые образы
docker-compose -f docker-compose.prod.yml build

# Применить миграции
docker-compose -f docker-compose.prod.yml exec backend alembic upgrade head

# Плавное обновление (по одному сервису)
docker-compose -f docker-compose.prod.yml up -d --no-deps --build backend
docker-compose -f docker-compose.prod.yml up -d --no-deps --build celery_worker

# Проверить health
curl https://tehnadzor.ru/health
```

---

## 📈 Шаг 8: Масштабирование

### 8.1 Увеличение workers

```bash
# Увеличить количество Celery workers
docker-compose -f docker-compose.prod.yml up -d --scale celery_worker=4

# Увеличить uvicorn workers в backend
# Отредактировать docker-compose.prod.yml:
# command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 8
```

### 8.2 Добавление replicas (Docker Swarm)

```bash
# Инициализация Swarm
docker swarm init

# Deploy stack
docker stack deploy -c docker-compose.prod.yml tehnadzor

# Масштабирование
docker service scale tehnadzor_backend=3
docker service scale tehnadzor_celery_worker=5
```

---

## 🛡️ Безопасность

### Checklist безопасности:

- [ ] Использовать сильные пароли для всех сервисов
- [ ] Включить SSL/TLS (HTTPS)
- [ ] Настроить firewall (UFW/iptables)
- [ ] Отключить root SSH логин
- [ ] Использовать SSH keys вместо паролей
- [ ] Регулярно обновлять систему и Docker образы
- [ ] Настроить fail2ban
- [ ] Ограничить доступ к портам БД (только внутри Docker network)
- [ ] Включить rate limiting в nginx
- [ ] Настроить логирование и мониторинг

---

## 📞 Troubleshooting

### Проблема: Сервисы не запускаются

```bash
# Проверить логи
docker-compose -f docker-compose.prod.yml logs

# Проверить ресурсы
docker stats

# Перезапустить все
docker-compose -f docker-compose.prod.yml restart
```

### Проблема: БД недоступна

```bash
# Проверить статус PostgreSQL
docker exec tehnadzor_postgres pg_isready

# Проверить подключение
docker exec tehnadzor_postgres psql -U postgres -c "SELECT 1"

# Пересоздать БД container
docker-compose -f docker-compose.prod.yml up -d --force-recreate postgres
```

### Проблема: Медленная работа

```bash
# Проверить нагрузку
htop

# Проверить диск
df -h
iostat

# Увеличить workers
# См. раздел "Масштабирование"
```

---

## ✅ Production Checklist

Перед запуском в production:

- [ ] Все тесты проходят (backend + mobile)
- [ ] SSL сертификат установлен
- [ ] .env файл настроен с production credentials
- [ ] Firewall настроен
- [ ] Backup настроен и протестирован
- [ ] Мониторинг настроен (Sentry, logs)
- [ ] Health checks работают
- [ ] Email настроен и протестирован
- [ ] AI API ключи добавлены
- [ ] Домен настроен и работает
- [ ] Nginx reverse proxy настроен
- [ ] Rate limiting включен
- [ ] CORS правильно настроен

---

**Версия:** 1.2.0
**Дата:** 08.11.2025
**Статус:** Ready for Production Deployment
