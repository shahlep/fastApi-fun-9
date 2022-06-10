from fastapi.testclient import TestClient
import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest
from config.settings import Settings

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app
from database import Base, get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
Test_Session_Local = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


@pytest.fixture
def client():
    def override_get_db():
        try:
            db = Test_Session_Local()
            yield db
        finally:
            db.close()

    # overrides
    app.dependency_overrides[get_db] = override_get_db

    client = TestClient(app)
    yield client


@pytest.fixture
def token_header(client: TestClient):
    data = {"username": Settings.TEST_EMAIL, "password": Settings.TEST_PASSWORD}
    response = client.post("/login/token", data=data)
    access_token = response.json()["access_token"]
    return {"Authorization": f"Bearer {access_token}"}
