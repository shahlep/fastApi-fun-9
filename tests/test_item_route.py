import json
from config.settings import Settings


def test_create_item(client, token_header):
    data = {"title": Settings.TEST_ITEM_TITLE, "description": Settings.TEST_ITEM_DESC}
    response = client.post("/items", json.dumps(data), headers=token_header)
    assert response.status_code == 200
    assert response.json()["title"] == Settings.TEST_ITEM_TITLE
    assert response.json()["description"] == Settings.TEST_ITEM_DESC


def test_get_item_by_id(client):
    response = client.get("/items/1")
    assert response.status_code == 200
    assert response.json()["title"] == Settings.TEST_ITEM_TITLE
    assert response.json()["description"] == Settings.TEST_ITEM_DESC
