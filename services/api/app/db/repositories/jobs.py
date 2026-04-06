from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.enums import ProcessingJobStatus
from app.domain.job_processing import transition_job_status
from app.domain.models import ProcessingJob


def list_jobs_by_project(session: Session, project_id: UUID) -> list[ProcessingJob]:
    statement = (
        select(ProcessingJob)
        .where(ProcessingJob.project_id == project_id)
        .order_by(ProcessingJob.created_at.desc())
    )
    return list(session.scalars(statement))


def get_job(session: Session, job_id: UUID) -> ProcessingJob | None:
    return session.get(ProcessingJob, job_id)


def create_job(session: Session, data: dict[str, object]) -> ProcessingJob:
    job = ProcessingJob(**data)
    session.add(job)
    session.commit()
    session.refresh(job)
    return job


def update_job_status(
    session: Session,
    job: ProcessingJob,
    status: ProcessingJobStatus,
) -> ProcessingJob:
    transition_job_status(
        session=session,
        job_id=job.id,
        project_id=job.project_id,
        requested_stems=job.requested_stems,
        status=status.value,
    )
    session.refresh(job)
    return job
