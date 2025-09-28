import uuid
from fastapi.testclient import TestClient

from sfasset_service.main import app


client = TestClient(app)


def test_create_entity():
    name = str(uuid.uuid4()).replace("-", "")
    response = client.post(
        "/projects/",
        json={"name": name},
    )
    data = response.json()
    project_id = data["id"]
    assert project_id

    entity_name = "myentity"

    response = client.post(
        "/entities/", json={"name": entity_name, "project_id": project_id}
    )
    data = response.json()
    assert data["name"] == entity_name


def test_create_child_entity():
    name = str(uuid.uuid4()).replace("-", "")
    response = client.post(
        "/projects/",
        json={"name": name},
    )
    data = response.json()
    project_id = data["id"]
    assert project_id

    response = client.post(
        "/entities/", json={"name": "parent", "project_id": project_id}
    )
    parent_data = response.json()
    assert parent_data["name"] == "parent"

    response = client.post(
        "/entities/",
        json={
            "name": "child",
            "project_id": project_id,
            "parent_id": parent_data["id"],
        },
    )
    child_data = response.json()
    assert child_data["name"] == "child"
    assert child_data["parent_id"] == parent_data["id"]
