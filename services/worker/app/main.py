import importlib.util
import logging
from pathlib import Path
import time
from typing import Any

from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session, sessionmaker

from app.core.settings import get_settings
from app.metrics import collect_startup_metrics

settings = get_settings()

logging.basicConfig(level=settings.log_level)
logger = logging.getLogger(settings.worker_name)

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


def _load_transition_job_status() -> Any:
    module_path = Path(__file__).resolve().parents[2] / "api/app/domain/job_processing.py"
    spec = importlib.util.spec_from_file_location("api_job_processing", module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load shared job processing module from {module_path}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.transition_job_status


transition_job_status = _load_transition_job_status()


def fetch_next_queued_job(session: Session) -> dict[str, Any] | None:
    row = session.execute(
        text(
            """
            SELECT id, project_id, requested_stems
            FROM processing_jobs
            WHERE status = :status
            ORDER BY created_at ASC
            LIMIT 1
            FOR UPDATE SKIP LOCKED
            """
        ),
        {"status": "queued"},
    ).mappings().first()
    if row is None:
        return None

    return dict(row)


def process_next_job() -> bool:
    with SessionLocal() as session:
        job = fetch_next_queued_job(session)
        if job is None:
            session.rollback()
            logger.debug("Nenhum job queued encontrado neste ciclo")
            return False

        logger.info(
            "Job queued encontrado",
            extra={"job_id": str(job["id"]), "project_id": str(job["project_id"])},
        )
        transition_job_status(
            session=session,
            job_id=job["id"],
            project_id=job["project_id"],
            requested_stems=job["requested_stems"],
            status="running",
        )
        logger.info("Job marcado como running", extra={"job_id": str(job["id"])})

    time.sleep(settings.processing_delay_seconds)

    with SessionLocal() as session:
        transition_job_status(
            session=session,
            job_id=job["id"],
            project_id=job["project_id"],
            requested_stems=job["requested_stems"],
            status="succeeded",
        )
        logger.info("Job marcado como succeeded", extra={"job_id": str(job["id"])})

    return True


def main() -> None:
    metrics = collect_startup_metrics(settings.worker_name)
    logger.info(
        "Worker automatico iniciado",
        extra={
            "worker_name": settings.worker_name,
            "environment": settings.environment,
            "metrics": metrics,
            "polling_interval_seconds": settings.polling_interval_seconds,
            "processing_delay_seconds": settings.processing_delay_seconds,
        },
    )

    while True:
        try:
            processed = process_next_job()
        except Exception:
            logger.exception("Falha ao processar ciclo do worker")
            time.sleep(settings.polling_interval_seconds)
            continue

        if not processed:
            time.sleep(settings.polling_interval_seconds)


if __name__ == "__main__":
    main()
