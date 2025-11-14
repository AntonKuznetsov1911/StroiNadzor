# Nginx Configuration - ТехНадзор

## Описание

Nginx конфигурация для production развертывания с поддержкой:

- ✅ SSL/TLS (HTTPS)
- ✅ HTTP/2
- ✅ Rate limiting (защита от DDoS)
- ✅ Gzip сжатие
- ✅ Reverse proxy для backend API
- ✅ Security headers
- ✅ Автоматический редирект HTTP → HTTPS

## Структура

```
nginx/
├── nginx.conf          # Основная конфигурация
├── ssl/                # Директория для SSL сертификатов (не в git)
│   ├── fullchain.pem   # SSL сертификат (создается отдельно)
│   └── privkey.pem     # Приватный ключ (создается отдельно)
├── .gitignore          # Исключает сертификаты из git
└── README.md           # Эта документация
```

## Настройка SSL сертификата

### Вариант 1: Let's Encrypt (рекомендуется для production)

```bash
# 1. Установите certbot
sudo apt install certbot python3-certbot-nginx -y

# 2. Остановите nginx если запущен
docker-compose -f docker-compose.prod.yml stop nginx

# 3. Получите сертификат (замените tehnadzor.ru на ваш домен)
sudo certbot certonly --standalone -d tehnadzor.ru -d www.tehnadzor.ru

# 4. Скопируйте сертификаты в проект
sudo cp /etc/letsencrypt/live/tehnadzor.ru/fullchain.pem ./nginx/ssl/
sudo cp /etc/letsencrypt/live/tehnadzor.ru/privkey.pem ./nginx/ssl/

# 5. Установите права доступа
sudo chmod 644 ./nginx/ssl/*.pem

# 6. Запустите nginx
docker-compose -f docker-compose.prod.yml up -d nginx
```

### Вариант 2: Самоподписанный сертификат (для development/testing)

```bash
# 1. Создайте директорию для сертификатов
mkdir -p nginx/ssl

# 2. Сгенерируйте самоподписанный сертификат
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout nginx/ssl/privkey.pem \
  -out nginx/ssl/fullchain.pem \
  -subj "/C=RU/ST=Moscow/L=Moscow/O=TehNadzor/CN=localhost"

# 3. Установите права
chmod 644 nginx/ssl/*.pem
```

**⚠️ Внимание:** Самоподписанные сертификаты вызовут предупреждения в браузере. Используйте только для development!

### Автоматическое обновление Let's Encrypt

Добавьте в cron для автоматического обновления сертификатов:

```bash
# Откройте crontab
sudo crontab -e

# Добавьте строку (обновление каждый месяц)
0 0 1 * * certbot renew --quiet && docker-compose -f /path/to/StroiNadzor/docker-compose.prod.yml restart nginx
```

## Rate Limiting

Конфигурация включает защиту от перегрузки:

- **API endpoints**: 10 запросов/сек (burst 20)
- **Auth endpoints**: 5 запросов/мин (burst 5)
- **Connections limit**: 10 одновременных подключений

Настройте эти значения в `nginx.conf`:

```nginx
limit_req_zone $binary_remote_addr zone=api_limit:10m rate=10r/s;
limit_req_zone $binary_remote_addr zone=auth_limit:10m rate=5r/m;
limit_conn_zone $binary_remote_addr zone=conn_limit:10m;
```

## Безопасность

### Security Headers

Включены следующие заголовки безопасности:

- `X-Frame-Options: SAMEORIGIN` - защита от clickjacking
- `X-Content-Type-Options: nosniff` - защита от MIME sniffing
- `X-XSS-Protection: 1; mode=block` - защита от XSS
- `Referrer-Policy: no-referrer-when-downgrade` - контроль referrer

### HSTS (HTTP Strict Transport Security)

После проверки работы SSL раскомментируйте строку в `nginx.conf`:

```nginx
add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload" always;
```

## Оптимизация

### Gzip сжатие

Включено для следующих типов:
- text/plain, text/css, text/xml, text/javascript
- application/json, application/javascript
- application/xml, image/svg+xml

### Кэширование

Статические файлы кэшируются на 7 дней:

```nginx
location /static/ {
    expires 7d;
    add_header Cache-Control "public, immutable";
}
```

## Мониторинг

### Проверка статуса

```bash
# Проверить синтаксис конфигурации
docker-compose -f docker-compose.prod.yml exec nginx nginx -t

# Перезагрузить конфигурацию без простоя
docker-compose -f docker-compose.prod.yml exec nginx nginx -s reload

# Просмотр логов
docker-compose -f docker-compose.prod.yml logs -f nginx
```

### Health Check

```bash
# Проверить доступность
curl -f https://yourdomain.ru/health
```

## Production Checklist

Перед запуском в production:

- [ ] SSL сертификат установлен от Let's Encrypt
- [ ] HSTS header раскомментирован и протестирован
- [ ] Swagger docs закомментирован (`/docs`, `/redoc`)
- [ ] Настроен автоматический renewal сертификатов
- [ ] Rate limiting настроен под вашу нагрузку
- [ ] Логи настроены и ротируются
- [ ] Домен правильно указан в `server_name`
- [ ] Firewall настроен (порты 80, 443 открыты)

## Дополнительные настройки

### Увеличение лимитов для больших файлов

Если нужно загружать файлы >100MB, измените:

```nginx
client_max_body_size 500M;  # Увеличить до 500MB
```

### Настройка для нескольких доменов

```nginx
server {
    listen 443 ssl http2;
    server_name domain1.ru www.domain1.ru;
    # ... настройки
}

server {
    listen 443 ssl http2;
    server_name domain2.ru www.domain2.ru;
    # ... настройки
}
```

## Troubleshooting

### Ошибка: "SSL certificate problem"

```bash
# Проверьте права доступа к сертификатам
ls -la nginx/ssl/

# Должно быть:
# -rw-r--r-- fullchain.pem
# -rw-r--r-- privkey.pem
```

### Ошибка: "502 Bad Gateway"

```bash
# Проверьте доступность backend
docker-compose -f docker-compose.prod.yml ps backend

# Проверьте логи
docker-compose -f docker-compose.prod.yml logs backend
```

### Ошибка: "413 Request Entity Too Large"

Увеличьте `client_max_body_size` в конфигурации nginx.

## Полезные команды

```bash
# Проверка конфигурации
make health

# Просмотр логов nginx
make prod-logs

# Перезапуск nginx
docker-compose -f docker-compose.prod.yml restart nginx
```

---

**Версия:** 1.0
**Дата:** 08.11.2025
