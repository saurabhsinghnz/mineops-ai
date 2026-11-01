from fastapi.testclient import TestClient

from app.main import app
from app.services import equipment_service

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_list_equipment():
    response = client.get("/api/v1/equipment")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["asset_code"] == "HT-102"

def test_empty_equipment_response(monkeypatch):
    monkeypatch.setattr(equipment_service, "equipment_data", [])

    response = client.get("/api/v1/equipment")
    assert response.status_code == 200
    assert response.json() == []

def test_get_equipment():
    response = client.get("/api/v1/equipment/1")
    assert response.status_code == 200
    data = response.json()
    assert data["asset_code"] == "HT-102"


def test_unknown_equipment():
    response = client.get("/api/v1/equipment/999")
    assert response.status_code == 404
