import json


def test_create_user():
    data = {"email": "test2@example.com", "password": "testuser3"}
    response = client.post("/users", json.dumps(data))
    assert response.status_code == 200
    assert response.json()["email"] == "test2@example.com"
    assert response.json()["is_active"] == True
