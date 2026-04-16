from __future__ import annotations

import logging
from pathlib import Path

from alembic.config import Config
from alembic.script import ScriptDirectory
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, sessionmaker

from app.core.settings import get_settings

settings = get_settings()
logger = logging.getLogger(__name__)

engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
    class_=Session,
)


def check_db_revision(db_engine: Engine | None = None) -> bool:
    active_engine = db_engine or engine

    try:
        alembic_config = Config(str(Path(__file__).resolve().parents[2] / "alembic.ini"))
        alembic_config.set_main_option("sqlalchemy.url", settings.database_url)
        script = ScriptDirectory.from_config(alembic_config)
        head_revision = script.get_current_head()

        with active_engine.connect() as connection:
            current_revision = connection.exec_driver_sql(
                "SELECT version_num FROM alembic_version"
            ).scalar_one_or_none()

        if current_revision != head_revision:
            logger.warning(
                "db_revision_not_at_head",
                extra={
                    "current_revision": current_revision,
                    "head_revision": head_revision,
                },
            )
            return False

        return True
    except SQLAlchemyError as error:
        logger.warning(
            "db_revision_check_failed",
            extra={"error": str(error)},
        )
        return False
