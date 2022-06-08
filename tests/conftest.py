from fastapi.testclient import TestClient
import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app

client = TestClient(app)

from database import Base, get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
Test_Session_Local = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = Test_Session_Local()
        yield db
    finally:
        db.close()


# overrides
app.dependency_overrides[get_db] = override_get_db
