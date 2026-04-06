from dataclasses import dataclass
from functools import lru_cache
import os
from pathlib import Path

from dotenv import load_dotenv

ENV_FILE = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(ENV_FILE)

@dataclass(frozen=True)
class Settings:
    worker_name: str = "music-stems-worker"
    environment: str = "local"
    log_level: str = "INFO"
    database_url: str = "postgresql+psycopg://music_stems:music_stems@localhost:5432/music_stems"
    redis_url: str = "redis://localhost:6379/0"
    polling_interval_seconds: float = 2.0
    processing_delay_seconds: float = 3.0


@lru_cache
def get_settings() -> Settings:
    return Settings(
        worker_name=os.getenv("WORKER_NAME", Settings.worker_name),
        environment=os.getenv("APP_ENV", Settings.environment),
        log_level=os.getenv("WORKER_LOG_LEVEL", Settings.log_level),
        database_url=os.getenv("DATABASE_URL", Settings.database_url),
        redis_url=os.getenv("REDIS_URL", Settings.redis_url),
        polling_interval_seconds=float(
            os.getenv("WORKER_POLLING_INTERVAL_SECONDS", str(Settings.polling_interval_seconds))
        ),
        processing_delay_seconds=float(
            os.getenv("WORKER_PROCESSING_DELAY_SECONDS", str(Settings.processing_delay_seconds))
        ),
    )
