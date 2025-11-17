"""
Middleware для FastAPI приложения
"""
import time
import logging
from typing import Callable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

# Настройка логгера
logger = logging.getLogger(__name__)


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware для логирования всех HTTP запросов
    """

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Начало обработки запроса
        start_time = time.time()

        # Получаем информацию о запросе
        method = request.method
        url = str(request.url)
        client_host = request.client.host if request.client else "unknown"

        # Обрабатываем запрос
        try:
            response = await call_next(request)

            # Вычисляем время обработки
            process_time = time.time() - start_time

            # Логируем успешный запрос
            logger.info(
                f"{method} {url} - Status: {response.status_code} - "
                f"Client: {client_host} - Time: {process_time:.3f}s"
            )

            # Добавляем заголовок с временем обработки
            response.headers["X-Process-Time"] = str(process_time)

            return response

        except Exception as exc:
            # Логируем ошибку
            process_time = time.time() - start_time
            logger.error(
                f"{method} {url} - Error: {str(exc)} - "
                f"Client: {client_host} - Time: {process_time:.3f}s",
                exc_info=True
            )
            raise


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    Middleware для добавления security headers
    """

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        response = await call_next(request)

        # Добавляем security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"

        return response


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Простой rate limiting middleware (in-memory)
    Для production используйте Redis-based решение
    """

    def __init__(self, app: ASGIApp, requests_per_minute: int = 60):
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        self.requests = {}  # {ip: [(timestamp, count)]}

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        client_ip = request.client.host if request.client else "unknown"
        current_time = time.time()

        # Очищаем старые записи (старше 1 минуты)
        if client_ip in self.requests:
            self.requests[client_ip] = [
                (timestamp, count)
                for timestamp, count in self.requests[client_ip]
                if current_time - timestamp < 60
            ]

        # Подсчитываем количество запросов за последнюю минуту
        request_count = sum(
            count for _, count in self.requests.get(client_ip, [])
        )

        # Проверяем лимит
        if request_count >= self.requests_per_minute:
            logger.warning(
                f"Rate limit exceeded for {client_ip} - "
                f"{request_count} requests in last minute"
            )
            return Response(
                content="Too many requests",
                status_code=429,
                headers={
                    "Retry-After": "60",
                    "X-RateLimit-Limit": str(self.requests_per_minute),
                    "X-RateLimit-Remaining": "0"
                }
            )

        # Добавляем текущий запрос
        if client_ip not in self.requests:
            self.requests[client_ip] = []
        self.requests[client_ip].append((current_time, 1))

        # Обрабатываем запрос
        response = await call_next(request)

        # Добавляем rate limit headers
        remaining = max(0, self.requests_per_minute - request_count - 1)
        response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
        response.headers["X-RateLimit-Remaining"] = str(remaining)

        return response


class DatabaseSessionMiddleware(BaseHTTPMiddleware):
    """
    Middleware для автоматического управления database сессиями
    """

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        try:
            # Добавляем информацию о начале транзакции
            request.state.db_session_started = time.time()

            response = await call_next(request)

            # Логируем время работы с БД
            if hasattr(request.state, "db_session_started"):
                db_time = time.time() - request.state.db_session_started
                if db_time > 1.0:  # Если запрос к БД > 1 секунды
                    logger.warning(
                        f"Slow database query: {request.url.path} - {db_time:.3f}s"
                    )

            return response

        except Exception as exc:
            logger.error(f"Database error: {str(exc)}", exc_info=True)
            raise


class CORSDebugMiddleware(BaseHTTPMiddleware):
    """
    Middleware для отладки CORS проблем (только для development)
    """

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Логируем CORS preflight requests
        if request.method == "OPTIONS":
            logger.debug(
                f"CORS Preflight: {request.url.path} - "
                f"Origin: {request.headers.get('origin', 'none')}"
            )

        response = await call_next(request)

        # Логируем CORS headers в response
        if request.headers.get("origin"):
            logger.debug(
                f"CORS Response headers: "
                f"Access-Control-Allow-Origin: {response.headers.get('access-control-allow-origin', 'none')}"
            )

        return response


class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    """
    Улучшенный middleware для обработки ошибок
    """

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        try:
            response = await call_next(request)
            return response

        except ValueError as exc:
            logger.error(f"Validation error: {str(exc)}", exc_info=True)
            return Response(
                content=f'{{"detail": "Validation error: {str(exc)}"}}',
                status_code=400,
                media_type="application/json"
            )

        except PermissionError as exc:
            logger.error(f"Permission denied: {str(exc)}", exc_info=True)
            return Response(
                content=f'{{"detail": "Permission denied: {str(exc)}"}}',
                status_code=403,
                media_type="application/json"
            )

        except FileNotFoundError as exc:
            logger.error(f"Resource not found: {str(exc)}", exc_info=True)
            return Response(
                content=f'{{"detail": "Resource not found: {str(exc)}"}}',
                status_code=404,
                media_type="application/json"
            )

        except TimeoutError as exc:
            logger.error(f"Request timeout: {str(exc)}", exc_info=True)
            return Response(
                content=f'{{"detail": "Request timeout", "error": "{str(exc)}"}}',
                status_code=504,
                media_type="application/json"
            )

        except Exception as exc:
            logger.critical(f"Unhandled exception: {str(exc)}", exc_info=True)
            return Response(
                content='{"detail": "Internal server error"}',
                status_code=500,
                media_type="application/json"
            )


class RequestIDMiddleware(BaseHTTPMiddleware):
    """
    Middleware для добавления уникального ID к каждому запросу
    """

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        import uuid

        # Генерируем уникальный ID запроса
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id

        # Добавляем request_id в логи
        logger.info(f"Request ID: {request_id} - {request.method} {request.url.path}")

        response = await call_next(request)

        # Добавляем request_id в response headers
        response.headers["X-Request-ID"] = request_id

        return response


class CompressionMiddleware(BaseHTTPMiddleware):
    """
    Middleware для включения compression headers
    """

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        response = await call_next(request)

        # Добавляем headers для compression
        if "gzip" in request.headers.get("accept-encoding", ""):
            response.headers["Content-Encoding"] = "gzip"

        return response


class CacheControlMiddleware(BaseHTTPMiddleware):
    """
    Middleware для установки cache-control headers
    """

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        response = await call_next(request)

        # Для статических файлов - длительный кеш
        if request.url.path.startswith("/static"):
            response.headers["Cache-Control"] = "public, max-age=31536000"
        # Для API - без кеша
        elif request.url.path.startswith("/api"):
            response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
            response.headers["Pragma"] = "no-cache"
            response.headers["Expires"] = "0"

        return response
