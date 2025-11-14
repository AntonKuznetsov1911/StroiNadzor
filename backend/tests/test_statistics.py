"""
Тесты для endpoints статистики
"""
import pytest
from fastapi.testclient import TestClient
from datetime import datetime


def test_get_dashboard_stats(client: TestClient):
    """Тест получения статистики дашборда"""
    response = client.get("/api/v1/statistics/dashboard")

    assert response.status_code == 200
    data = response.json()

    # Проверка структуры ответа
    assert "summary" in data
    assert "projects_by_status" in data
    assert "inspections_by_result" in data

    # Проверка полей summary
    summary = data["summary"]
    assert "total_projects" in summary
    assert "active_projects" in summary
    assert "total_inspections" in summary
    assert "total_defects" in summary
    assert "critical_defects" in summary
    assert "pending_hidden_works" in summary

    # Проверка типов данных
    assert isinstance(summary["total_projects"], int)
    assert isinstance(summary["active_projects"], int)
    assert isinstance(summary["total_defects"], int)


def test_get_project_statistics(client: TestClient):
    """Тест получения статистики по проекту"""
    project_id = 1
    response = client.get(f"/api/v1/statistics/project/{project_id}")

    assert response.status_code == 200
    data = response.json()

    # Проверка структуры
    assert "project_id" in data
    assert "project_name" in data
    assert "completion_percentage" in data
    assert "inspections" in data
    assert "photos" in data
    assert "defects" in data
    assert "hidden_works" in data

    # Проверка вложенных структур
    assert "total" in data["inspections"]
    assert "by_result" in data["inspections"]
    assert "by_type" in data["defects"]
    assert "by_severity" in data["defects"]


def test_get_project_statistics_not_found(client: TestClient):
    """Тест статистики несуществующего проекта"""
    response = client.get("/api/v1/statistics/project/99999")

    assert response.status_code == 200
    data = response.json()
    assert "error" in data


def test_get_trends(client: TestClient):
    """Тест получения трендов"""
    response = client.get("/api/v1/statistics/trends?days=7")

    assert response.status_code == 200
    data = response.json()

    assert "period_days" in data
    assert "inspections_trend" in data
    assert "defects_trend" in data

    assert data["period_days"] == 7
    assert isinstance(data["inspections_trend"], list)
    assert isinstance(data["defects_trend"], list)

    # Проверка структуры элементов тренда
    if len(data["inspections_trend"]) > 0:
        trend_item = data["inspections_trend"][0]
        assert "date" in trend_item
        assert "count" in trend_item


def test_get_trends_default_days(client: TestClient):
    """Тест получения трендов с параметром по умолчанию"""
    response = client.get("/api/v1/statistics/trends")

    assert response.status_code == 200
    data = response.json()
    assert data["period_days"] == 30  # Значение по умолчанию


@pytest.mark.parametrize("days", [1, 7, 14, 30, 90])
def test_get_trends_various_periods(client: TestClient, days: int):
    """Тест трендов для разных периодов"""
    response = client.get(f"/api/v1/statistics/trends?days={days}")

    assert response.status_code == 200
    data = response.json()
    assert data["period_days"] == days
