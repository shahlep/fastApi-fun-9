import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path("") / ".env"
load_dotenv(dotenv_path=env_path)


class Settings:
    app_title: str = "My Application"
    app_version: str = "0.1.1"
    api_json_version: str = "/api/v1/openapi.json"
    app_description: str = "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum."

    tags = [
        {"name": "User", "description": "User Related Routes"},
        {"name": "Items", "description": "Item Related Routes"},
    ]
    POSTGRESS_USER: str = os.getenv("POSTGRESS_USER")
    POSTGRESS_PASSWORD: str = os.getenv("POSTGRESS_PASSWORD")
    POSTGRESS_SERVER: str = os.getenv("POSTGRESS_SERVER", "localhost")
    POSTGRESS_PORT: str = os.getenv("POSTGRESS_PORT", 5432)
    POSTGRESS_DB: str = os.getenv("POSTGRESS_DB")
    DATABASE_URL = f"postgresql://{POSTGRESS_USER}:{POSTGRESS_PASSWORD}@{POSTGRESS_SERVER}:{POSTGRESS_PORT}/{POSTGRESS_DB}"

    SECURITY_KEY = os.getenv("SECURITY_KEY")

settings = Settings()
