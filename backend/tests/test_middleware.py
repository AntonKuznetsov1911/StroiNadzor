"""
Тесты для middleware компонентов
"""
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.middleware import (
    RequestLoggingMiddleware,
    SecurityHeadersMiddleware,
    RequestIDMiddleware,
    CacheControlMiddleware,
    ErrorHandlingMiddleware
)


@pytest.fixture
def app():
    """Фикстура FastAPI приложения"""
    app = FastAPI()

    @app.get("/test")
    def test_endpoint():
        return {"message": "success"}

    @app.get("/error")
    def error_endpoint():
        raise ValueError("Test error")

    @app.get("/api/data")
    def api_endpoint():
        return {"data": "test"}

    @app.get("/static/file.js")
    def static_endpoint():
        return {"file": "content"}

    return app


class TestRequestLoggingMiddleware:
    """Тесты для RequestLoggingMiddleware"""

    def test_logging_middleware(self, app):
        app.add_middleware(RequestLoggingMiddleware)
        client = TestClient(app)

        response = client.get("/test")

        assert response.status_code == 200
        assert "X-Process-Time" in response.headers
        assert float(response.headers["X-Process-Time"]) >= 0


class TestSecurityHeadersMiddleware:
    """Тесты для SecurityHeadersMiddleware"""

    def test_security_headers(self, app):
        app.add_middleware(SecurityHeadersMiddleware)
        client = TestClient(app)

        response = client.get("/test")

        assert response.status_code == 200
        assert response.headers["X-Content-Type-Options"] == "nosniff"
        assert response.headers["X-Frame-Options"] == "DENY"
        assert response.headers["X-XSS-Protection"] == "1; mode=block"
        assert "Strict-Transport-Security" in response.headers


class TestRequestIDMiddleware:
    """Тесты для RequestIDMiddleware"""

    def test_request_id_generation(self, app):
        app.add_middleware(RequestIDMiddleware)
        client = TestClient(app)

        response = client.get("/test")

        assert response.status_code == 200
        assert "X-Request-ID" in response.headers

        request_id = response.headers["X-Request-ID"]
        assert len(request_id) == 36  # UUID length with dashes

    def test_unique_request_ids(self, app):
        app.add_middleware(RequestIDMiddleware)
        client = TestClient(app)

        response1 = client.get("/test")
        response2 = client.get("/test")

        id1 = response1.headers["X-Request-ID"]
        id2 = response2.headers["X-Request-ID"]

        assert id1 != id2


class TestCacheControlMiddleware:
    """Тесты для CacheControlMiddleware"""

    def test_api_no_cache(self, app):
        app.add_middleware(CacheControlMiddleware)
        client = TestClient(app)

        response = client.get("/api/data")

        assert response.status_code == 200
        assert response.headers["Cache-Control"] == "no-cache, no-store, must-revalidate"
        assert response.headers["Pragma"] == "no-cache"
        assert response.headers["Expires"] == "0"

    def test_static_cache(self, app):
        app.add_middleware(CacheControlMiddleware)
        client = TestClient(app)

        response = client.get("/static/file.js")

        assert response.status_code == 200
        assert "max-age=31536000" in response.headers["Cache-Control"]


class TestErrorHandlingMiddleware:
    """Тесты для ErrorHandlingMiddleware"""

    def test_value_error_handling(self, app):
        app.add_middleware(ErrorHandlingMiddleware)
        client = TestClient(app)

        response = client.get("/error")

        assert response.status_code == 400
        assert "detail" in response.json()
        assert "Validation error" in response.json()["detail"]


class TestMiddlewareStack:
    """Тесты для совместной работы middleware"""

    def test_multiple_middleware(self, app):
        # Добавляем несколько middleware
        app.add_middleware(SecurityHeadersMiddleware)
        app.add_middleware(RequestIDMiddleware)
        app.add_middleware(RequestLoggingMiddleware)

        client = TestClient(app)
        response = client.get("/test")

        # Проверяем, что все middleware сработали
        assert response.status_code == 200
        assert "X-Request-ID" in response.headers
        assert "X-Process-Time" in response.headers
        assert "X-Content-Type-Options" in response.headers


@pytest.mark.parametrize("endpoint,expected_status", [
    ("/test", 200),
    ("/api/data", 200),
    ("/static/file.js", 200),
])
def test_middleware_with_different_endpoints(app, endpoint, expected_status):
    """Тест middleware с разными endpoints"""
    app.add_middleware(RequestLoggingMiddleware)
    app.add_middleware(SecurityHeadersMiddleware)

    client = TestClient(app)
    response = client.get(endpoint)

    assert response.status_code == expected_status
    assert "X-Process-Time" in response.headers
    assert "X-Content-Type-Options" in response.headers
