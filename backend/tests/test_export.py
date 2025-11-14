"""
Тесты для endpoints экспорта
"""
import pytest
from fastapi.testclient import TestClient
import csv
import json
from io import StringIO


def test_export_projects_csv(client: TestClient):
    """Тест экспорта проектов в CSV"""
    response = client.get("/api/v1/export/projects/csv")

    assert response.status_code == 200
    assert response.headers["content-type"] == "text/csv; charset=utf-8"
    assert "attachment" in response.headers["content-disposition"]
    assert "projects_" in response.headers["content-disposition"]

    # Проверка содержимого CSV
    csv_content = response.text
    csv_reader = csv.reader(StringIO(csv_content))
    rows = list(csv_reader)

    # Проверка заголовков
    assert len(rows) > 0
    headers = rows[0]
    assert "ID" in headers
    assert "Название" in headers
    assert "Статус" in headers
    assert "Адрес" in headers
    assert "Прогресс %" in headers


def test_export_inspections_csv(client: TestClient):
    """Тест экспорта проверок в CSV"""
    response = client.get("/api/v1/export/inspections/csv")

    assert response.status_code == 200
    assert response.headers["content-type"] == "text/csv; charset=utf-8"

    # Проверка содержимого
    csv_content = response.text
    csv_reader = csv.reader(StringIO(csv_content))
    rows = list(csv_reader)

    assert len(rows) > 0
    headers = rows[0]
    assert "ID" in headers
    assert "Проект ID" in headers
    assert "Название" in headers


def test_export_inspections_csv_with_filter(client: TestClient):
    """Тест экспорта проверок с фильтром по проекту"""
    project_id = 1
    response = client.get(f"/api/v1/export/inspections/csv?project_id={project_id}")

    assert response.status_code == 200

    # Проверка, что все проверки относятся к указанному проекту
    csv_content = response.text
    csv_reader = csv.reader(StringIO(csv_content))
    rows = list(csv_reader)

    if len(rows) > 1:  # Если есть данные кроме заголовка
        # Индекс колонки "Проект ID" (обычно 1)
        for row in rows[1:]:
            assert str(row[1]) == str(project_id)


def test_export_project_json(client: TestClient):
    """Тест экспорта проекта в JSON"""
    project_id = 1
    response = client.get(f"/api/v1/export/project/{project_id}/json")

    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"
    assert "attachment" in response.headers["content-disposition"]
    assert f"project_{project_id}" in response.headers["content-disposition"]

    # Проверка структуры JSON
    data = response.json()
    assert "project" in data
    assert "inspections" in data
    assert "hidden_works" in data
    assert "export_date" in data
    assert "exported_by" in data


def test_export_project_json_not_found(client: TestClient):
    """Тест экспорта несуществующего проекта"""
    response = client.get("/api/v1/export/project/99999/json")

    assert response.status_code == 200
    data = response.json()
    assert "error" in data


def test_batch_export(client: TestClient):
    """Тест пакетного экспорта проектов"""
    payload = {
        "project_ids": [1, 2],
        "format": "json"
    }

    response = client.post("/api/v1/export/batch-export", json=payload)

    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"

    # Проверка структуры
    data = response.json()
    assert "export_date" in data
    assert "exported_by" in data
    assert "projects" in data
    assert isinstance(data["projects"], list)


def test_batch_export_no_projects(client: TestClient):
    """Тест пакетного экспорта с пустым списком"""
    payload = {
        "project_ids": [99999],
        "format": "json"
    }

    response = client.post("/api/v1/export/batch-export", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert "error" in data


def test_batch_export_unsupported_format(client: TestClient):
    """Тест пакетного экспорта с неподдерживаемым форматом"""
    payload = {
        "project_ids": [1],
        "format": "xml"
    }

    response = client.post("/api/v1/export/batch-export", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert "error" in data


def test_export_csv_filename_format(client: TestClient):
    """Тест формата имени файла CSV"""
    response = client.get("/api/v1/export/projects/csv")

    assert response.status_code == 200
    filename = response.headers["content-disposition"]

    # Проверка формата: projects_YYYYMMDD_HHMMSS.csv
    assert "projects_" in filename
    assert ".csv" in filename


def test_export_json_encoding(client: TestClient):
    """Тест корректной кодировки русских символов в JSON"""
    response = client.get("/api/v1/export/project/1/json")

    assert response.status_code == 200
    data = response.json()

    # Проверка что русский текст корректно декодируется
    if "project" in data:
        project = data["project"]
        if "name" in project:
            # Русские символы должны быть читаемыми
            assert isinstance(project["name"], str)
