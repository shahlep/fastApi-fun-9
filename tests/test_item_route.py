import json


def test_create_item():
    data = {"title": "test title", "description": "test description"}
    response = client.post("/items", json.dumps(data))
    assert response.status_code == 200
    assert response.json()["title"] == "test title"
    assert response.json()["description"] == "test description"
