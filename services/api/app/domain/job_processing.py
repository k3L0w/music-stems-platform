from __future__ import annotations

from collections.abc import Sequence
from uuid import UUID, uuid4

from sqlalchemy import text
from sqlalchemy.orm import Session

PROJECT_STATUS_BY_JOB_STATUS = {
    "queued": "uploaded",
    "running": "processing",
    "succeeded": "completed",
    "failed": "failed",
}


def transition_job_status(
    session: Session,
    *,
    job_id: UUID,
    project_id: UUID,
    requested_stems: Sequence[str],
    status: str,
) -> None:
    project_status = PROJECT_STATUS_BY_JOB_STATUS.get(status)
    if project_status is None:
        raise ValueError(f"Unsupported job status transition: {status}")

    session.execute(
        text(
            """
            UPDATE processing_jobs
            SET status = :status
            WHERE id = :job_id
            """
        ),
        {"status": status, "job_id": job_id},
    )
    session.execute(
        text(
            """
            UPDATE projects
            SET status = :project_status
            WHERE id = :project_id
            """
        ),
        {"project_status": project_status, "project_id": project_id},
    )

    if status == "succeeded":
        _create_missing_placeholder_stems(
            session=session,
            job_id=job_id,
            project_id=project_id,
            requested_stems=requested_stems,
        )

    session.commit()


def _create_missing_placeholder_stems(
    session: Session,
    *,
    job_id: UUID,
    project_id: UUID,
    requested_stems: Sequence[str],
) -> None:
    existing_stem_types = set(
        session.execute(
            text(
                """
                SELECT stem_type
                FROM generated_stems
                WHERE processing_job_id = :job_id
                """
            ),
            {"job_id": job_id},
        ).scalars()
    )

    for stem_type in requested_stems:
        if stem_type in existing_stem_types:
            continue

        session.execute(
            text(
                """
                INSERT INTO generated_stems (
                    id,
                    project_id,
                    processing_job_id,
                    stem_type,
                    file_key,
                    created_at
                )
                VALUES (
                    :id,
                    :project_id,
                    :job_id,
                    :stem_type,
                    :file_key,
                    NOW()
                )
                """
            ),
            {
                "id": uuid4(),
                "project_id": project_id,
                "job_id": job_id,
                "stem_type": stem_type,
                "file_key": f"projects/{project_id}/jobs/{job_id}/{stem_type}.wav",
            },
        )
