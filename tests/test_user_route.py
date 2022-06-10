import json
from config.settings import Settings


def test_create_user(client):
    data = {"email": Settings.TEST_EMAIL, "password": Settings.TEST_PASSWORD}
    response = client.post("/users", json.dumps(data))
    assert response.status_code == 200
    assert response.json()["email"] == Settings.TEST_EMAIL
    assert response.json()["is_active"] == True
