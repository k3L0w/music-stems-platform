from collections.abc import Callable
from datetime import datetime
import logging
from typing import Any, Dict, List

from app.domain.models import GeneratedStem, ProcessingJob, Project

logger = logging.getLogger(__name__)


def load_project_timeline(
    *,
    project: Project,
    jobs_loader: Callable[[], List[ProcessingJob]],
    stems_loader: Callable[[], List[GeneratedStem]],
) -> List[Dict[str, Any]]:
    project_id = getattr(project, "id", "unknown")
    jobs = _safe_load_collection(
        loader=jobs_loader,
        project_id=project_id,
        label="jobs",
    )
    stems = _safe_load_collection(
        loader=stems_loader,
        project_id=project_id,
        label="stems",
    )
    return build_project_timeline(project=project, jobs=jobs, stems=stems)


def build_project_timeline(
    *,
    project: Project,
    jobs: List[ProcessingJob] | None,
    stems: List[GeneratedStem] | None,
) -> List[Dict[str, Any]]:
    project_id = getattr(project, "id", "unknown")
    jobs = jobs or []
    stems = stems or []
    events: List[Dict[str, Any]] = []

    try:
        events.append(
            {
                "type": "project_created",
                "timestamp": project.created_at,
                "title": "Projeto criado",
                "description": f"Projeto {project.name} criado com status inicial {project.status}.",
            }
        )
    except Exception as error:
        _log_error("project_created", project_id, error)

    for job in jobs:
        try:
            events.append(_event_job_created(job))

            if job.started_at:
                events.append(_event_job_started(job))

            if job.status == "running" and job.started_at:
                events.append(_event_job_running(job))

            if job.status == "succeeded" and job.finished_at:
                events.append(_event_job_succeeded(job))

            if job.status == "failed" and job.finished_at:
                events.append(_event_job_failed(job))
        except Exception as error:
            _log_error("job_event", project_id, error)

    for stem in stems:
        try:
            if stem.created_at:
                events.append(
                    {
                        "type": "stem_generated",
                        "timestamp": stem.created_at,
                        "title": f"Stem {stem.stem_type} gerado",
                        "description": f"Stem {stem.stem_type} disponível para download.",
                        "job_id": stem.processing_job_id,
                        "stem_id": stem.id,
                    }
                )
        except Exception as error:
            _log_error("stem_event", project_id, error)

    valid_events = _filter_valid_events(events, project_id)
    deduplicated_events = _deduplicate_events(valid_events)

    try:
        return sorted(deduplicated_events, key=_sort_key)
    except Exception as error:
        _log_error("timeline_sort", project_id, error)
        return deduplicated_events


# =========================
# 🔧 EVENT BUILDERS
# =========================

def _event_job_created(job: ProcessingJob) -> Dict[str, Any]:
    requested = ", ".join(job.requested_stems or [])
    return {
        "type": "job_created",
        "timestamp": _resolve_timestamp(
            finished_at=getattr(job, "finished_at", None),
            started_at=getattr(job, "started_at", None),
            created_at=getattr(job, "created_at", None),
        ),
        "title": "Job criado",
        "description": f"Job {job.provider} criado para stems: {requested}.",
        "job_id": job.id,
    }


def _event_job_started(job: ProcessingJob) -> Dict[str, Any]:
    return {
        "type": "job_started",
        "timestamp": _resolve_timestamp(
            finished_at=None,
            started_at=getattr(job, "started_at", None),
            created_at=getattr(job, "created_at", None),
        ),
        "title": "Job iniciado",
        "description": f"Processamento iniciado no provider {job.provider}.",
        "job_id": job.id,
    }


def _event_job_running(job: ProcessingJob) -> Dict[str, Any]:
    return {
        "type": "job_running",
        "timestamp": _resolve_timestamp(
            finished_at=None,
            started_at=getattr(job, "started_at", None),
            created_at=getattr(job, "created_at", None),
        ),
        "title": "Job em execução",
        "description": "O processamento está em andamento.",
        "job_id": job.id,
    }


def _event_job_succeeded(job: ProcessingJob) -> Dict[str, Any]:
    return {
        "type": "job_succeeded",
        "timestamp": _resolve_timestamp(
            finished_at=getattr(job, "finished_at", None),
            started_at=getattr(job, "started_at", None),
            created_at=getattr(job, "created_at", None),
        ),
        "title": "Job concluído",
        "description": "Processamento concluído com sucesso.",
        "job_id": job.id,
    }


def _event_job_failed(job: ProcessingJob) -> Dict[str, Any]:
    return {
        "type": "job_failed",
        "timestamp": _resolve_timestamp(
            finished_at=getattr(job, "finished_at", None),
            started_at=getattr(job, "started_at", None),
            created_at=getattr(job, "created_at", None),
        ),
        "title": "Job falhou",
        "description": "O processamento falhou.",
        "job_id": job.id,
    }


# =========================
# 🔃 SORT
# =========================

def _sort_key(event: Dict[str, Any]) -> tuple:
    return (
        event.get("timestamp") or datetime.min,
        str(event.get("type")),
        str(event.get("job_id") or event.get("stem_id") or ""),
    )


def _safe_load_collection(
    *,
    loader: Callable[[], List[Any]],
    project_id: object,
    label: str,
) -> List[Any]:
    try:
        return loader() or []
    except Exception as error:
        _log_error(f"{label}_query", project_id, error)
        return []


def _resolve_timestamp(
    *,
    finished_at: datetime | None,
    started_at: datetime | None,
    created_at: datetime | None,
) -> datetime | None:
    return finished_at or started_at or created_at


def _filter_valid_events(events: List[Dict[str, Any]], project_id: object) -> List[Dict[str, Any]]:
    valid_events: List[Dict[str, Any]] = []

    for event in events:
        try:
            if not isinstance(event, dict):
                raise TypeError("Timeline event is not a dict.")
            event["timestamp"] = _resolve_timestamp(
                finished_at=event.get("finished_at"),
                started_at=event.get("started_at"),
                created_at=event.get("timestamp"),
            )
            if event.get("timestamp") is None:
                raise ValueError("Timeline event timestamp is missing.")
            if not event.get("type"):
                raise ValueError("Timeline event type is missing.")
            if not event.get("title"):
                raise ValueError("Timeline event title is missing.")
            if not event.get("description"):
                raise ValueError("Timeline event description is missing.")

            valid_events.append(event)
        except Exception as error:
            _log_error("timeline_event_validation", project_id, error)

    return valid_events


def _deduplicate_events(events: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    deduplicated_events: List[Dict[str, Any]] = []
    seen_keys: set[tuple[str, datetime, str, str]] = set()

    for event in events:
        timestamp = event.get("timestamp")
        if timestamp is None:
            continue

        event_key = (
            str(event.get("type")),
            timestamp,
            str(event.get("job_id") or ""),
            str(event.get("stem_id") or ""),
        )
        if event_key in seen_keys:
            continue

        seen_keys.add(event_key)
        deduplicated_events.append(event)

    return deduplicated_events


def _log_error(context: str, project_id: object, error: Exception) -> None:
    logger.error(
        context,
        extra={
            "project_id": str(project_id),
            "error": str(error),
        },
        exc_info=error,
    )
