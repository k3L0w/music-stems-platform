from dataclasses import dataclass
from functools import lru_cache
import os
from pathlib import Path

from dotenv import load_dotenv

ENV_FILE = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(ENV_FILE)


@dataclass(frozen=True)
class Settings:
    app_name: str = "Music Stems Platform API"
    app_description: str = "Base tecnica inicial da API do projeto."
    app_version: str = "0.1.0"
    environment: str = "local"
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    docs_url: str = "/docs"
    database_url: str = "postgresql+psycopg://music_stems:music_stems@localhost:5432/music_stems"
    redis_url: str = "redis://localhost:6379/0"


@lru_cache
def get_settings() -> Settings:
    return Settings(
        app_name=os.getenv("APP_NAME", Settings.app_name),
        app_description=os.getenv("APP_DESCRIPTION", Settings.app_description),
        app_version=os.getenv("APP_VERSION", Settings.app_version),
        environment=os.getenv("APP_ENV", Settings.environment),
        api_host=os.getenv("API_HOST", Settings.api_host),
        api_port=int(os.getenv("API_PORT", str(Settings.api_port))),
        docs_url=os.getenv("API_DOCS_URL", Settings.docs_url),
        database_url=os.getenv("DATABASE_URL", Settings.database_url),
        redis_url=os.getenv("REDIS_URL", Settings.redis_url),
    )
