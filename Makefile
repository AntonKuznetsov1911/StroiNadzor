# Makefile для упрощения команд проекта ТехНадзор

.PHONY: help setup start stop restart logs clean test

# Цвета для вывода
BLUE := \033[0;34m
GREEN := \033[0;32m
YELLOW := \033[1;33m
NC := \033[0m # No Color

help: ## Показать эту справку
	@echo "$(BLUE)ТехНадзор - Доступные команды:$(NC)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-15s$(NC) %s\n", $$1, $$2}'

# === Docker команды ===

setup: ## Первичная настройка проекта
	@echo "$(YELLOW)Настройка проекта...$(NC)"
	@cp backend/.env.example backend/.env || echo "backend/.env уже существует"
	@docker-compose build
	@echo "$(GREEN)Настройка завершена!$(NC)"
	@echo "Отредактируйте backend/.env и запустите 'make start'"

start: ## Запустить все сервисы
	@echo "$(YELLOW)Запуск сервисов...$(NC)"
	@docker-compose up -d
	@echo "$(GREEN)Сервисы запущены!$(NC)"
	@echo "Backend API: http://localhost:8000"
	@echo "Swagger docs: http://localhost:8000/docs"
	@echo "MinIO console: http://localhost:9001"

stop: ## Остановить все сервисы
	@echo "$(YELLOW)Остановка сервисов...$(NC)"
	@docker-compose down
	@echo "$(GREEN)Сервисы остановлены$(NC)"

restart: stop start ## Перезапустить все сервисы

logs: ## Показать логи всех сервисов
	@docker-compose logs -f

logs-backend: ## Показать логи backend
	@docker-compose logs -f backend

logs-celery: ## Показать логи celery worker
	@docker-compose logs -f celery

# === Backend команды ===

backend-shell: ## Запустить Python shell в backend контейнере
	@docker-compose exec backend python

backend-migrate: ## Применить миграции БД
	@echo "$(YELLOW)Применение миграций...$(NC)"
	@docker-compose exec backend alembic upgrade head
	@echo "$(GREEN)Миграции применены$(NC)"

backend-migration: ## Создать новую миграцию (использовать: make backend-migration MSG="описание")
	@docker-compose exec backend alembic revision --autogenerate -m "$(MSG)"

backend-init-data: ## Инициализировать тестовые данные
	@echo "$(YELLOW)Инициализация тестовых данных...$(NC)"
	@docker-compose exec backend python scripts/init_data.py
	@echo "$(GREEN)Данные инициализированы$(NC)"

backend-test: ## Запустить тесты backend
	@docker-compose exec backend pytest tests/ -v

# === Mobile команды ===

mobile-install: ## Установить зависимости для mobile
	@echo "$(YELLOW)Установка зависимостей...$(NC)"
	@cd mobile && npm install
	@echo "$(GREEN)Зависимости установлены$(NC)"

mobile-start: ## Запустить Metro bundler
	@cd mobile && npm start

mobile-android: ## Запустить на Android
	@cd mobile && npm run android

mobile-ios: ## Запустить на iOS
	@cd mobile && npm run ios

mobile-test: ## Запустить тесты mobile
	@cd mobile && npm test

mobile-lint: ## Проверить код mobile
	@cd mobile && npm run lint

# === Очистка ===

clean: ## Очистить временные файлы и volumes
	@echo "$(YELLOW)Очистка...$(NC)"
	@docker-compose down -v
	@rm -rf backend/__pycache__
	@rm -rf backend/.pytest_cache
	@rm -rf mobile/node_modules
	@echo "$(GREEN)Очистка завершена$(NC)"

clean-db: ## Очистить базу данных (ОСТОРОЖНО!)
	@echo "$(YELLOW)ВНИМАНИЕ: Все данные будут удалены!$(NC)"
	@docker-compose down -v postgres
	@docker volume rm stroinadzor_postgres_data || true

# === Разработка ===

dev-backend: ## Запустить backend в dev режиме
	@cd backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

dev-full: ## Запустить полный стек для разработки
	@echo "$(YELLOW)Запуск dev окружения...$(NC)"
	@docker-compose up -d postgres redis elasticsearch minio
	@echo "$(GREEN)Инфраструктура запущена$(NC)"
	@echo "Теперь запустите backend и mobile вручную"

# === Утилиты ===

ps: ## Показать статус контейнеров
	@docker-compose ps

db-psql: ## Подключиться к PostgreSQL
	@docker-compose exec postgres psql -U tehnadzor -d tehnadzor_db

db-redis: ## Подключиться к Redis CLI
	@docker-compose exec redis redis-cli

# === Production ===

prod-build: ## Собрать production образы
	@echo "$(YELLOW)Сборка production образов...$(NC)"
	@docker-compose -f docker-compose.prod.yml build
	@echo "$(GREEN)Образы собраны$(NC)"

prod-deploy: ## Запустить в production режиме
	@echo "$(YELLOW)Запуск в production режиме...$(NC)"
	@docker-compose -f docker-compose.prod.yml up -d
	@echo "$(GREEN)Production запущен$(NC)"

prod-stop: ## Остановить production
	@echo "$(YELLOW)Остановка production...$(NC)"
	@docker-compose -f docker-compose.prod.yml down
	@echo "$(GREEN)Production остановлен$(NC)"

prod-logs: ## Показать логи production
	@docker-compose -f docker-compose.prod.yml logs -f

prod-migrate: ## Применить миграции в production
	@echo "$(YELLOW)Применение миграций в production...$(NC)"
	@docker-compose -f docker-compose.prod.yml exec backend alembic upgrade head
	@echo "$(GREEN)Миграции применены$(NC)"

prod-backup: ## Создать backup БД
	@echo "$(YELLOW)Создание backup...$(NC)"
	@mkdir -p backups
	@docker-compose -f docker-compose.prod.yml exec -T postgres pg_dump -U postgres tehnadzor > backups/backup_$(shell date +%Y%m%d_%H%M%S).sql
	@echo "$(GREEN)Backup создан$(NC)"

prod-restore: ## Восстановить БД из backup (использовать: make prod-restore FILE=backup.sql)
	@echo "$(YELLOW)Восстановление из backup...$(NC)"
	@docker-compose -f docker-compose.prod.yml exec -T postgres psql -U postgres tehnadzor < $(FILE)
	@echo "$(GREEN)БД восстановлена$(NC)"

prod-scale-celery: ## Масштабировать celery workers (использовать: make prod-scale-celery N=4)
	@docker-compose -f docker-compose.prod.yml up -d --scale celery_worker=$(N)
	@echo "$(GREEN)Celery workers масштабированы до $(N)$(NC)"

health: ## Проверить health всех сервисов
	@echo "$(YELLOW)Проверка health сервисов...$(NC)"
	@curl -f http://localhost:8000/health || echo "Backend: FAILED"
	@curl -f http://localhost:9000/minio/health/live || echo "MinIO: FAILED"
	@docker-compose exec postgres pg_isready || echo "PostgreSQL: FAILED"
	@docker-compose exec redis redis-cli ping || echo "Redis: FAILED"
	@echo "$(GREEN)Проверка завершена$(NC)"

demo: ## Запустить demo server без Docker
	@echo "$(YELLOW)Запуск demo server...$(NC)"
	@cd backend && python demo_server.py

# === Monitoring ===

monitoring-start: ## Запустить мониторинг (Prometheus + Grafana)
	@echo "$(YELLOW)Запуск мониторинга...$(NC)"
	@docker-compose -f docker-compose.prod.yml -f docker-compose.monitoring.yml up -d
	@echo "$(GREEN)Мониторинг запущен!$(NC)"
	@echo "Grafana: http://localhost:3000 (admin/admin123)"
	@echo "Prometheus: http://localhost:9090"
	@echo "Alertmanager: http://localhost:9093"

monitoring-stop: ## Остановить мониторинг
	@echo "$(YELLOW)Остановка мониторинга...$(NC)"
	@docker-compose -f docker-compose.monitoring.yml down
	@echo "$(GREEN)Мониторинг остановлен$(NC)"

monitoring-logs: ## Логи мониторинга
	@docker-compose -f docker-compose.monitoring.yml logs -f

monitoring-prometheus: ## Открыть Prometheus UI
	@echo "Открытие Prometheus..."
	@echo "http://localhost:9090"

monitoring-grafana: ## Открыть Grafana UI
	@echo "Открытие Grafana..."
	@echo "http://localhost:3000"
	@echo "Login: admin / Password: admin123"
