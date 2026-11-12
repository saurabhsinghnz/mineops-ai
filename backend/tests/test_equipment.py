import pytest
from app.api.dependencies import get_db
from app.api.routes import equipment as equipment_route
from app.main import app
from app.models.equipment import Equipment
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

client = TestClient(app)


class TestHealth:
    def test_health_check(self):
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"


class TestGetEquipment:
    def test_list_equipment(self, create_client, db, equipment_data):
        created = create_client.post("/api/v1/equipment", json=equipment_data)
        assert created.status_code == 201
        second = Equipment(
            asset_code="PMP-201",
            name="Water Pump 201",
            equipment_type="Water Pump",
            site="Site B",
        )
        db.add(second)
        db.commit()
        db.refresh(second)

        response = create_client.get("/api/v1/equipment")
        assert response.status_code == 200
        assert sorted(response.json(), key=lambda item: item["id"]) == [
            created.json(),
            {
                "id": second.id,
                "asset_code": "PMP-201",
                "name": "Water Pump 201",
                "equipment_type": "Water Pump",
                "site": "Site B",
                "manufacturer": None,
                "model": None,
            },
        ]

    def test_empty_equipment_response(self, create_client):
        response = create_client.get("/api/v1/equipment")
        assert response.status_code == 200
        assert response.json() == []

    def test_get_equipment(self, create_client, equipment_data):
        created = create_client.post(
            "/api/v1/equipment",
            json={**equipment_data, "asset_code": "DB-001", "name": "Database asset"},
        )
        assert created.status_code == 201

        response = create_client.get(f"/api/v1/equipment/{created.json()['id']}")
        assert response.status_code == 200
        assert response.json() == created.json()

    @pytest.mark.parametrize("equipment_id", [1, 999])
    def test_unknown_equipment(self, create_client, equipment_id):
        response = create_client.get(f"/api/v1/equipment/{equipment_id}")
        assert response.status_code == 404
        assert response.json() == {"detail": "Equipment not found"}


@pytest.fixture
def db():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Equipment.__table__.create(engine)
    with Session(engine) as session:
        yield session
    engine.dispose()


@pytest.fixture
def create_client(db):
    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db
    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.pop(get_db, None)


@pytest.fixture
def equipment_data():
    return {
        "asset_code": "HT-102",
        "name": "Haul Truck 102",
        "equipment_type": "Haul Truck",
        "site": "Site A",
        "manufacturer": "Caterpillar",
        "model": "793F",
    }


class TestPostEquipment:
    @pytest.mark.parametrize("include_optional", [True, False])
    def test_create_equipment(
        self, create_client, db, equipment_data, include_optional
    ):
        if not include_optional:
            equipment_data.pop("manufacturer")
            equipment_data.pop("model")

        response = create_client.post("/api/v1/equipment", json=equipment_data)

        assert response.status_code == 201
        expected = {"manufacturer": None, "model": None, **equipment_data}
        body = response.json()
        assert body == {"id": 1, **expected}
        saved = db.get(Equipment, body["id"])
        assert saved is not None
        assert {key: getattr(saved, key) for key in expected} == expected

    def test_duplicate_asset_code_returns_conflict_and_rolls_back(
        self, create_client, db, equipment_data
    ):
        first = create_client.post("/api/v1/equipment", json=equipment_data)
        duplicate = create_client.post(
            "/api/v1/equipment", json={**equipment_data, "name": "Different name"}
        )

        assert first.status_code == 201
        assert duplicate.status_code == 409
        assert duplicate.json() == {"detail": "Asset code already exists"}
        saved = db.scalars(select(Equipment)).all()
        assert len(saved) == 1
        assert saved[0].name == equipment_data["name"]

        next_response = create_client.post(
            "/api/v1/equipment", json={**equipment_data, "asset_code": "HT-103"}
        )
        assert next_response.status_code == 201
        assert next_response.json()["asset_code"] == "HT-103"

    @pytest.mark.parametrize(
        "missing_field", ["asset_code", "name", "equipment_type", "site"]
    )
    def test_create_equipment_rejects_missing_required_field(
        self, create_client, db, equipment_data, missing_field
    ):
        equipment_data.pop(missing_field)

        response = create_client.post("/api/v1/equipment", json=equipment_data)

        assert response.status_code == 422
        assert any(
            error["loc"] == ["body", missing_field] and error["type"] == "missing"
            for error in response.json()["detail"]
        )
        assert db.scalars(select(Equipment)).all() == []

    def test_unrelated_integrity_error_is_rolled_back_and_reraised(
        self, create_client, db, equipment_data, monkeypatch
    ):
        error = IntegrityError("INSERT", {}, Exception("other constraint"))
        rollback_calls = []
        original_rollback = db.rollback

        def rollback():
            rollback_calls.append(True)
            original_rollback()

        def fail_create(db, data):
            raise error

        monkeypatch.setattr(db, "rollback", rollback)
        monkeypatch.setattr(equipment_route, "create_equipment", fail_create)

        with pytest.raises(IntegrityError) as raised:
            create_client.post("/api/v1/equipment", json=equipment_data)

        assert raised.value is error
        assert rollback_calls == [True]
