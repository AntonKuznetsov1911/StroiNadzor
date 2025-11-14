# Руководство по развертыванию "ТехНадзор"

## Production Deployment

### Требования

- Сервер Linux (Ubuntu 20.04+ рекомендуется)
- Docker и Docker Compose
- Домен с SSL сертификатом
- Минимум 4GB RAM, 2 CPU cores
- 50GB+ дискового пространства

---

## 1. Подготовка сервера

```bash
# Обновление системы
sudo apt update && sudo apt upgrade -y

# Установка Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Установка Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Добавление пользователя в группу docker
sudo usermod -aG docker $USER
```

---

## 2. Клонирование проекта

```bash
cd /opt
sudo git clone https://github.com/your-org/tehnadzor.git
cd tehnadzor
```

---

## 3. Конфигурация окружения

```bash
# Создание .env файла
cd backend
sudo cp .env.example .env
sudo nano .env
```

### Обязательные параметры в .env:

```env
# Production Database
DATABASE_URL=postgresql://tehnadzor:STRONG_PASSWORD@postgres:5432/tehnadzor_db

# Redis
REDIS_URL=redis://redis:6379/0

# Security
SECRET_KEY=GENERATE_STRONG_SECRET_KEY_HERE
DEBUG=False

# API Keys
OPENAI_API_KEY=your-openai-key
CLAUDE_API_KEY=your-claude-key

# CORS
CORS_ORIGINS=https://yourdomain.com,https://app.yourdomain.com

# Email
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

**Генерация SECRET_KEY:**
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

---

## 4. SSL сертификаты

### Использование Let's Encrypt

```bash
# Установка Certbot
sudo apt install certbot

# Получение сертификата
sudo certbot certonly --standalone -d api.yourdomain.com
```

Сертификаты будут в `/etc/letsencrypt/live/api.yourdomain.com/`

---

## 5. Nginx конфигурация

Создайте `/etc/nginx/sites-available/tehnadzor`:

```nginx
upstream backend {
    server localhost:8000;
}

server {
    listen 80;
    server_name api.yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name api.yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/api.yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/api.yourdomain.com/privkey.pem;

    # Security headers
    add_header Strict-Transport-Security "max-age=31536000" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;

    client_max_body_size 50M;

    location / {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /uploads {
        alias /opt/tehnadzor/backend/uploads;
    }
}
```

Активация конфигурации:
```bash
sudo ln -s /etc/nginx/sites-available/tehnadzor /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

---

## 6. Запуск приложения

```bash
cd /opt/tehnadzor

# Сборка и запуск
sudo docker-compose -f docker-compose.prod.yml up -d

# Проверка статуса
sudo docker-compose ps

# Просмотр логов
sudo docker-compose logs -f backend
```

---

## 7. Инициализация базы данных

```bash
# Применение миграций
sudo docker-compose exec backend alembic upgrade head

# Инициализация тестовых данных (опционально)
sudo docker-compose exec backend python scripts/init_data.py
```

---

## 8. Настройка автозапуска

Создайте systemd service `/etc/systemd/system/tehnadzor.service`:

```ini
[Unit]
Description=TehNadzor Application
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/opt/tehnadzor
ExecStart=/usr/local/bin/docker-compose -f docker-compose.prod.yml up -d
ExecStop=/usr/local/bin/docker-compose -f docker-compose.prod.yml down
TimeoutStartSec=0

[Install]
WantedBy=multi-user.target
```

Активация:
```bash
sudo systemctl daemon-reload
sudo systemctl enable tehnadzor
sudo systemctl start tehnadzor
```

---

## 9. Мониторинг

### Установка Prometheus и Grafana

```bash
# В docker-compose.prod.yml добавлены сервисы мониторинга
sudo docker-compose -f docker-compose.prod.yml up -d prometheus grafana

# Grafana доступна на http://your-ip:3000
# Логин: admin / admin
```

### Метрики приложения

- CPU и память контейнеров
- Время отклика API
- Количество запросов
- Ошибки и исключения

---

## 10. Backup и восстановление

### Автоматический backup

Создайте скрипт `/opt/tehnadzor/backup.sh`:

```bash
#!/bin/bash
BACKUP_DIR="/opt/backups/tehnadzor"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

# Backup PostgreSQL
docker-compose exec -T postgres pg_dump -U tehnadzor tehnadzor_db | gzip > $BACKUP_DIR/db_$DATE.sql.gz

# Backup uploads
tar -czf $BACKUP_DIR/uploads_$DATE.tar.gz backend/uploads/

# Удаление старых бэкапов (старше 30 дней)
find $BACKUP_DIR -type f -mtime +30 -delete

echo "Backup completed: $DATE"
```

Добавьте в crontab:
```bash
sudo crontab -e

# Ежедневный backup в 2:00
0 2 * * * /opt/tehnadzor/backup.sh >> /var/log/tehnadzor_backup.log 2>&1
```

### Восстановление из backup

```bash
# Восстановление БД
gunzip -c /opt/backups/tehnadzor/db_20251107_020000.sql.gz | \
  docker-compose exec -T postgres psql -U tehnadzor tehnadzor_db

# Восстановление файлов
tar -xzf /opt/backups/tehnadzor/uploads_20251107_020000.tar.gz
```

---

## 11. Обновление приложения

```bash
cd /opt/tehnadzor

# Получить последнюю версию
sudo git pull origin main

# Пересборка и перезапуск
sudo docker-compose -f docker-compose.prod.yml down
sudo docker-compose -f docker-compose.prod.yml build
sudo docker-compose -f docker-compose.prod.yml up -d

# Применить новые миграции
sudo docker-compose exec backend alembic upgrade head
```

---

## 12. Мобильное приложение

### iOS (App Store)

1. Настройте Xcode проект с правильным Bundle ID
2. Создайте Production сертификаты в Apple Developer
3. Обновите API URL в `mobile/src/config/api.ts`
4. Создайте Archive в Xcode
5. Загрузите через App Store Connect

### Android (Google Play)

1. Создайте keystore для подписи:
```bash
cd mobile/android/app
keytool -genkey -v -keystore tehnadzor.keystore \
  -alias tehnadzor -keyalg RSA -keysize 2048 -validity 10000
```

2. Настройте `android/gradle.properties`:
```
MYAPP_UPLOAD_STORE_FILE=tehnadzor.keystore
MYAPP_UPLOAD_KEY_ALIAS=tehnadzor
MYAPP_UPLOAD_STORE_PASSWORD=***
MYAPP_UPLOAD_KEY_PASSWORD=***
```

3. Соберите APK/AAB:
```bash
cd mobile/android
./gradlew bundleRelease
```

4. Загрузите в Google Play Console

---

## 13. Масштабирование

### Horizontal scaling

Для увеличения нагрузки добавьте несколько экземпляров backend:

```yaml
# docker-compose.prod.yml
backend:
  deploy:
    replicas: 3
```

### Load Balancer

Используйте Nginx или HAProxy для балансировки:

```nginx
upstream backend {
    least_conn;
    server backend1:8000;
    server backend2:8000;
    server backend3:8000;
}
```

---

## 14. Безопасность

### Checklist

- [ ] Изменены все пароли по умолчанию
- [ ] SSL сертификаты установлены
- [ ] Firewall настроен (ufw/iptables)
- [ ] Доступ к админ панелям ограничен по IP
- [ ] Регулярные обновления системы
- [ ] Backup настроен и протестирован
- [ ] Логи мониторятся
- [ ] Rate limiting включен
- [ ] CORS правильно настроен

### Firewall (UFW)

```bash
sudo ufw allow 22/tcp   # SSH
sudo ufw allow 80/tcp   # HTTP
sudo ufw allow 443/tcp  # HTTPS
sudo ufw enable
```

---

## 15. Troubleshooting

### Контейнер не запускается

```bash
# Просмотр логов
sudo docker-compose logs backend

# Проверка конфигурации
sudo docker-compose config

# Пересборка
sudo docker-compose build --no-cache backend
```

### База данных недоступна

```bash
# Проверка PostgreSQL
sudo docker-compose exec postgres pg_isready

# Проверка подключения
sudo docker-compose exec backend python -c "from app.database import engine; print(engine.connect())"
```

### Медленная работа

- Проверьте использование ресурсов: `docker stats`
- Оптимизируйте запросы к БД
- Настройте кэширование Redis
- Масштабируйте horizontally

---

## Контакты поддержки

- Email: support@tehnadzor.ru
- Telegram: @tehnadzor_support
- GitHub Issues: https://github.com/your-org/tehnadzor/issues

---

*Последнее обновление: 2025-11-07*
