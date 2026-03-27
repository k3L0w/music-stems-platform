from dataclasses import dataclass
from functools import lru_cache
import os


@dataclass(frozen=True)
class Settings:
    worker_name: str = "music-stems-worker"
    environment: str = "local"
    log_level: str = "INFO"
    database_url: str = "postgresql://music_stems:music_stems@localhost:5432/music_stems"
    redis_url: str = "redis://localhost:6379/0"


@lru_cache
def get_settings() -> Settings:
    return Settings(
        worker_name=os.getenv("WORKER_NAME", Settings.worker_name),
        environment=os.getenv("APP_ENV", Settings.environment),
        log_level=os.getenv("WORKER_LOG_LEVEL", Settings.log_level),
        database_url=os.getenv("DATABASE_URL", Settings.database_url),
        redis_url=os.getenv("REDIS_URL", Settings.redis_url),
    )
