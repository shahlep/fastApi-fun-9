from fastapi.testclient import TestClient
import json
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app

client = TestClient(app)


def test_create_user():
    data = {"email": "test1@example.com", "password": "testuser2"}
    response = client.post("/users", json.dumps(data))
    assert response.status_code == 200
    assert response.json()["email"] == "test1@example.com"
    assert response.json()["is_active"] == True
