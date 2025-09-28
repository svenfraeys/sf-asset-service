from fastapi.testclient import TestClient

from sfasset_service.main import app


client = TestClient(app)


def test_app():
    assert app


def test_create_project():
    response = client.post(
        "/projects/",
        json={"name": "test"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "test"
    assert "id" in data
