from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.schemas.jobs import JobCreateRequest, JobResponse
from app.db.dependencies import get_db_session
from app.db.repositories.jobs import create_job, get_job, list_jobs_by_project
from app.db.repositories.projects import get_project

router = APIRouter(tags=["jobs"])


@router.post("/projects/{project_id}/jobs", response_model=JobResponse, status_code=status.HTTP_201_CREATED)
def create_job_endpoint(
    project_id: UUID,
    payload: JobCreateRequest,
    session: Session = Depends(get_db_session),
) -> JobResponse:
    project = get_project(session=session, project_id=project_id)
    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found.")

    job = create_job(
        session=session,
        data={
            "project_id": project.id,
            "provider": payload.provider,
            "requested_stems": payload.requested_stems,
        },
    )
    return JobResponse.model_validate(job)


@router.get("/projects/{project_id}/jobs", response_model=list[JobResponse])
def read_project_jobs(
    project_id: UUID,
    session: Session = Depends(get_db_session),
) -> list[JobResponse]:
    project = get_project(session=session, project_id=project_id)
    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found.")

    jobs = list_jobs_by_project(session=session, project_id=project.id)
    return [JobResponse.model_validate(job) for job in jobs]


@router.get("/jobs/{job_id}", response_model=JobResponse)
def read_job(job_id: UUID, session: Session = Depends(get_db_session)) -> JobResponse:
    job = get_job(session=session, job_id=job_id)
    if job is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found.")

    return JobResponse.model_validate(job)
