"""
Тесты аутентификации
"""
import pytest


def test_register_user(client):
    """Тест регистрации нового пользователя"""
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "newuser@example.com",
            "password": "securepass123",
            "full_name": "New User",
            "role": "engineer"
        }
    )

    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "newuser@example.com"
    assert data["full_name"] == "New User"
    assert "id" in data


def test_register_duplicate_email(client, test_user):
    """Тест регистрации с существующим email"""
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": test_user.email,
            "password": "password123",
            "full_name": "Duplicate User",
            "role": "engineer"
        }
    )

    assert response.status_code == 400
    assert "already registered" in response.json()["detail"].lower()


def test_login_success(client, test_user):
    """Тест успешного входа"""
    response = client.post(
        "/api/v1/auth/login",
        data={"username": test_user.email, "password": "testpassword123"}
    )

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["user"]["email"] == test_user.email


def test_login_wrong_password(client, test_user):
    """Тест входа с неправильным паролем"""
    response = client.post(
        "/api/v1/auth/login",
        data={"username": test_user.email, "password": "wrongpassword"}
    )

    assert response.status_code == 401


def test_login_nonexistent_user(client):
    """Тест входа несуществующего пользователя"""
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "nonexistent@example.com", "password": "password123"}
    )

    assert response.status_code == 401


def test_get_current_user(client, auth_headers):
    """Тест получения информации о текущем пользователе"""
    response = client.get("/api/v1/auth/me", headers=auth_headers)

    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"


def test_get_current_user_no_token(client):
    """Тест получения информации без токена"""
    response = client.get("/api/v1/auth/me")

    assert response.status_code == 401
