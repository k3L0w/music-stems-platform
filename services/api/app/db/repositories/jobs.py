from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.enums import ProcessingJobStatus, ProjectStatus, StemType
from app.domain.models import GeneratedStem, ProcessingJob


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
    job.status = status

    project = job.project
    if status == ProcessingJobStatus.QUEUED:
        project.status = ProjectStatus.UPLOADED
    elif status == ProcessingJobStatus.RUNNING:
        project.status = ProjectStatus.PROCESSING
    elif status == ProcessingJobStatus.SUCCEEDED:
        project.status = ProjectStatus.COMPLETED
        _create_missing_placeholder_stems(session=session, job=job)
    elif status == ProcessingJobStatus.FAILED:
        project.status = ProjectStatus.FAILED

    session.add(project)
    session.add(job)
    session.commit()
    session.refresh(job)
    return job


def _create_missing_placeholder_stems(session: Session, job: ProcessingJob) -> None:
    existing_stem_types = {
        stem_type
        for stem_type in session.scalars(
            select(GeneratedStem.stem_type).where(GeneratedStem.processing_job_id == job.id)
        )
    }

    for requested_stem in job.requested_stems:
        stem_type = StemType(requested_stem)
        if stem_type in existing_stem_types:
            continue

        session.add(
            GeneratedStem(
                project_id=job.project_id,
                processing_job_id=job.id,
                stem_type=stem_type,
                file_key=f"projects/{job.project_id}/jobs/{job.id}/{stem_type.value}.wav",
            )
        )
