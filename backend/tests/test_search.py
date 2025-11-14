"""
Тесты для endpoints поиска
"""
import pytest
from fastapi.testclient import TestClient


def test_global_search(client: TestClient):
    """Тест глобального поиска"""
    response = client.get("/api/v1/search/global?q=горизонт")

    assert response.status_code == 200
    data = response.json()

    assert "query" in data
    assert "results" in data
    assert "total_results" in data

    # Проверка структуры результатов
    results = data["results"]
    assert "projects" in results
    assert "inspections" in results
    assert "hidden_works" in results
    assert "documents" in results

    assert isinstance(results["projects"], list)
    assert data["query"] == "горизонт"


def test_global_search_min_length_validation(client: TestClient):
    """Тест валидации минимальной длины запроса"""
    response = client.get("/api/v1/search/global?q=a")

    # Должна быть ошибка валидации
    assert response.status_code == 422


def test_global_search_no_results(client: TestClient):
    """Тест поиска без результатов"""
    response = client.get("/api/v1/search/global?q=несуществующийпроект12345")

    assert response.status_code == 200
    data = response.json()

    # Результаты должны быть пустыми
    assert data["total_results"] == 0


def test_search_projects(client: TestClient):
    """Тест поиска проектов"""
    response = client.get("/api/v1/search/projects?q=москва")

    assert response.status_code == 200
    data = response.json()

    assert "query" in data
    assert "filters" in data
    assert "results" in data
    assert "count" in data

    assert data["query"] == "москва"


def test_search_projects_with_status_filter(client: TestClient):
    """Тест поиска проектов с фильтром по статусу"""
    response = client.get("/api/v1/search/projects?q=горизонт&status=in_progress")

    assert response.status_code == 200
    data = response.json()

    assert data["filters"]["status"] == "in_progress"

    # Все результаты должны иметь статус in_progress
    for project in data["results"]:
        assert project["status"] == "in_progress"


def test_search_regulations(client: TestClient):
    """Тест поиска по нормативам"""
    response = client.get("/api/v1/search/regulations?q=бетон")

    assert response.status_code == 200
    data = response.json()

    assert "query" in data
    assert "results" in data
    assert "count" in data

    # Проверка структуры результата
    if len(data["results"]) > 0:
        regulation = data["results"][0]
        assert "id" in regulation
        assert "code" in regulation
        assert "title" in regulation
        assert "regulation_type" in regulation


def test_autocomplete(client: TestClient):
    """Тест автодополнения"""
    response = client.get("/api/v1/search/autocomplete?q=жк")

    assert response.status_code == 200
    data = response.json()

    assert "query" in data
    assert "suggestions" in data
    assert isinstance(data["suggestions"], list)

    # Проверка структуры suggestion
    if len(data["suggestions"]) > 0:
        suggestion = data["suggestions"][0]
        assert "text" in suggestion
        assert "type" in suggestion


def test_autocomplete_with_entity_type(client: TestClient):
    """Тест автодополнения с фильтром по типу"""
    response = client.get("/api/v1/search/autocomplete?q=п&entity_type=projects")

    assert response.status_code == 200
    data = response.json()

    # Все suggestions должны быть проектами
    for suggestion in data["suggestions"]:
        assert suggestion["type"] == "project"


def test_autocomplete_with_limit(client: TestClient):
    """Тест автодополнения с ограничением количества"""
    limit = 5
    response = client.get(f"/api/v1/search/autocomplete?q=п&limit={limit}")

    assert response.status_code == 200
    data = response.json()

    # Результатов не должно быть больше лимита
    assert len(data["suggestions"]) <= limit


@pytest.mark.parametrize("search_term", ["горизонт", "галерея", "бетон", "проверка"])
def test_global_search_various_terms(client: TestClient, search_term: str):
    """Тест глобального поиска с разными запросами"""
    response = client.get(f"/api/v1/search/global?q={search_term}")

    assert response.status_code == 200
    data = response.json()
    assert data["query"] == search_term
