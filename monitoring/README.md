# Monitoring Stack - ТехНадзор

## Описание

Полный стек мониторинга для production окружения на основе Prometheus и Grafana.

### Компоненты

- **Prometheus** - сбор и хранение метрик
- **Grafana** - визуализация метрик через дашборды
- **Alertmanager** - управление алертами и уведомлениями
- **Node Exporter** - метрики сервера (CPU, RAM, Disk, Network)
- **PostgreSQL Exporter** - метрики базы данных
- **Redis Exporter** - метрики Redis

## Быстрый старт

### 1. Запуск мониторинга

```bash
# Запустить production + monitoring
docker-compose -f docker-compose.prod.yml -f docker-compose.monitoring.yml up -d

# Или через Makefile
make monitoring-start
```

### 2. Доступ к интерфейсам

- **Grafana**: http://localhost:3000
  - Логин: `admin`
  - Пароль: `admin123` (измените в `.env`)

- **Prometheus**: http://localhost:9090
- **Alertmanager**: http://localhost:9093

### 3. Настройка Grafana

При первом входе:

1. Войдите с учетными данными admin/admin123
2. Смените пароль
3. Datasource (Prometheus) уже настроен автоматически
4. Импортируйте готовые дашборды (см. ниже)

## Структура

```
monitoring/
├── prometheus/
│   ├── prometheus.yml      # Конфигурация Prometheus
│   └── alerts.yml          # Правила алертов
├── grafana/
│   ├── datasources/        # Автоматическая настройка datasources
│   │   └── prometheus.yml
│   └── dashboards/         # Provisioning дашбордов
│       └── dashboard.yml
├── alertmanager/
│   └── alertmanager.yml    # Конфигурация уведомлений
└── README.md               # Эта документация
```

## Метрики

### Backend Metrics

Backend должен экспортировать метрики на `/metrics` endpoint.

Для добавления метрик в FastAPI, установите:

```bash
pip install prometheus-fastapi-instrumentator
```

И добавьте в `backend/app/main.py`:

```python
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI()

# После создания app
Instrumentator().instrument(app).expose(app)
```

### Собираемые метрики

#### System (Node Exporter)
- CPU usage, load average
- Memory usage
- Disk I/O, space
- Network traffic

#### PostgreSQL
- Connections count
- Queries per second
- Cache hit ratio
- Database size
- Replication lag

#### Redis
- Memory usage
- Connected clients
- Commands per second
- Hit/Miss ratio
- Evicted keys

#### Backend
- HTTP request rate
- Response time (p50, p95, p99)
- Error rate (4xx, 5xx)
- Active connections

## Алерты

### Настроенные алерты

**Critical:**
- Backend Down (1 min)
- PostgreSQL Down (1 min)
- Redis Down (1 min)
- Low Disk Space (<10%)

**Warning:**
- High Error Rate (>5% 5xx)
- High Response Time (p95 > 2s)
- High CPU Usage (>80% for 10min)
- High Memory Usage (>90%)
- High Database Connections (>80)

### Email уведомления

Настройте в `.env`:

```env
SMTP_HOST=smtp.gmail.com
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
ALERT_EMAIL=alerts@tehnadzor.ru
```

### Telegram уведомления (опционально)

1. Создайте бота через @BotFather
2. Получите токен бота
3. Раскомментируйте webhook в `alertmanager.yml`
4. Добавьте в `.env`:

```env
TELEGRAM_BOT_TOKEN=your-bot-token
TELEGRAM_CHAT_ID=your-chat-id
```

## Grafana Dashboards

### Импорт готовых дашбордов

1. Откройте Grafana (http://localhost:3000)
2. Перейдите в Dashboards → Import
3. Импортируйте дашборды по ID:

**Рекомендуемые дашборды:**

- **1860** - Node Exporter Full
- **9628** - PostgreSQL Database
- **11835** - Redis Dashboard
- **7645** - FastAPI

### Создание custom дашборда

Пример панели для Backend requests:

```
Query: rate(http_requests_total[5m])
Visualization: Time series
Title: Requests per second
```

## Retention

### Prometheus

Данные хранятся 30 дней (настроено в `docker-compose.monitoring.yml`):

```yaml
--storage.tsdb.retention.time=30d
```

Для изменения:

```yaml
--storage.tsdb.retention.time=90d  # 90 дней
--storage.tsdb.retention.size=50GB # или по размеру
```

### Grafana

Данные хранятся в volume `grafana_data`.

Для бэкапа настроек:

```bash
# Экспорт дашбордов
docker exec tehnadzor_grafana \
  curl -s http://admin:admin123@localhost:3000/api/search?query=& | \
  jq -r '.[] | .uid' | \
  xargs -I {} docker exec tehnadzor_grafana \
    curl -s http://admin:admin123@localhost:3000/api/dashboards/uid/{} > dashboard_{}.json
```

## Команды Makefile

Добавьте в Makefile:

```makefile
# Monitoring команды
monitoring-start: ## Запустить мониторинг
	@docker-compose -f docker-compose.prod.yml -f docker-compose.monitoring.yml up -d
	@echo "Grafana: http://localhost:3000 (admin/admin123)"
	@echo "Prometheus: http://localhost:9090"

monitoring-stop: ## Остановить мониторинг
	@docker-compose -f docker-compose.monitoring.yml down

monitoring-logs: ## Логи мониторинга
	@docker-compose -f docker-compose.monitoring.yml logs -f
```

## Troubleshooting

### Проблема: Prometheus не может подключиться к targets

```bash
# Проверьте, что все сервисы в одной сети
docker network inspect tehnadzor_network

# Проверьте логи Prometheus
docker logs tehnadzor_prometheus
```

### Проблема: Alertmanager не отправляет email

```bash
# Проверьте конфигурацию SMTP
docker logs tehnadzor_alertmanager

# Тестовый алерт
curl -XPOST http://localhost:9093/api/v1/alerts -d '[{
  "labels": {"alertname": "test", "severity": "warning"},
  "annotations": {"summary": "Test alert"}
}]'
```

### Проблема: Grafana не показывает данные

1. Проверьте datasource: Configuration → Data Sources
2. Проверьте доступность Prometheus: http://localhost:9090
3. Проверьте query в панели

## Best Practices

### 1. Регулярный мониторинг

- Проверяйте дашборды минимум раз в день
- Настройте алерты на критичные метрики
- Анализируйте тренды

### 2. Retention policy

- Храните детальные данные 30 дней
- Для долгосрочного хранения используйте downsampling

### 3. Безопасность

- Смените дефолтные пароли Grafana
- Ограничьте доступ к портам мониторинга через firewall
- Используйте HTTPS для Grafana в production

### 4. Backup

- Регулярно делайте backup Grafana дашбордов
- Бэкапьте Prometheus data при критичных изменениях

## Production Checklist

Перед запуском в production:

- [ ] Сменены дефолтные пароли Grafana
- [ ] Настроены email/telegram уведомления
- [ ] Алерты протестированы
- [ ] Импортированы все необходимые дашборды
- [ ] Настроен retention согласно требованиям
- [ ] Порты мониторинга защищены firewall
- [ ] Настроен backup Grafana
- [ ] Документированы все custom метрики

## Полезные ссылки

- [Prometheus Documentation](https://prometheus.io/docs/)
- [Grafana Documentation](https://grafana.com/docs/)
- [PromQL Tutorial](https://prometheus.io/docs/prometheus/latest/querying/basics/)
- [Grafana Dashboards](https://grafana.com/grafana/dashboards/)

---

**Версия:** 1.0
**Дата:** 08.11.2025
