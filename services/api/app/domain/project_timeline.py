from datetime import datetime

from app.domain.models import GeneratedStem, ProcessingJob, Project


def build_project_timeline(
    *,
    project: Project,
    jobs: list[ProcessingJob],
    stems: list[GeneratedStem],
) -> list[dict[str, object]]:
    events: list[dict[str, object]] = [
        {
            "type": "project_created",
            "timestamp": project.created_at,
            "title": "Projeto criado",
            "description": f"Projeto {project.name} criado com status inicial {project.status}.",
        }
    ]

    for job in jobs:
        events.append(_build_job_created_event(job))
        events.append(_build_job_status_event(job))

    for stem in stems:
        events.append(
            {
                "type": "stem_generated",
                "timestamp": stem.created_at,
                "title": f"Stem {stem.stem_type} gerado",
                "description": f"Stem placeholder {stem.stem_type} disponibilizado para download.",
                "job_id": stem.processing_job_id,
                "stem_id": stem.id,
            }
        )

    return sorted(events, key=_sort_key)


def _build_job_created_event(job: ProcessingJob) -> dict[str, object]:
    requested_stems = ", ".join(job.requested_stems)
    return {
        "type": "job_created",
        "timestamp": job.created_at,
        "title": "Job criado",
        "description": f"Job {job.provider} criado para stems: {requested_stems}.",
        "job_id": job.id,
    }


def _build_job_status_event(job: ProcessingJob) -> dict[str, object]:
    return {
        "type": "job_status",
        "timestamp": job.created_at,
        "title": f"Status atual observado: {job.status}",
        "description": (
            "Este evento usa o timestamp de criacao do job como referencia. "
            "A API ainda nao guarda timestamps separados para cada transicao de status."
        ),
        "job_id": job.id,
    }


def _sort_key(event: dict[str, object]) -> tuple[datetime, str, str]:
    return (
        event["timestamp"],
        str(event["type"]),
        str(event.get("job_id") or event.get("stem_id") or ""),
    )
