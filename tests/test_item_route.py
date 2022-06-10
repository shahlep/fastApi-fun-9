import json


def test_create_item(client, token_header):
    data = {"title": "test title", "description": "test description"}
    response = client.post("/items", json.dumps(data), headers=token_header)
    assert response.status_code == 200
    assert response.json()["title"] == "test title"
    assert response.json()["description"] == "test description"


def test_get_item_by_id(client):
    response = client.get("/items/1")
    assert response.status_code == 200
    assert response.json()["title"] == "test title"
    assert response.json()["description"] == "test description"
