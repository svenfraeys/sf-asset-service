import uuid
from fastapi.testclient import TestClient

from sfasset_service.main import app


client = TestClient(app)


def test_app():
    assert app


def test_create_project():
    name = str(uuid.uuid4()).replace("-", "")
    response = client.post(
        "/projects/",
        json={"name": name},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == name
    assert data["code"] == name
    assert "id" in data
