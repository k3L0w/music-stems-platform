from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.api.schemas.jobs import (
    JobCreateErrorCode,
    JobCreateErrorResponse,
    JobCreateRequest,
    JobResponse,
    JobStatusUpdateRequest,
)
from app.db.dependencies import get_db_session
from app.db.repositories.jobs import (
    count_active_jobs_by_user,
    create_job,
    get_job,
    list_jobs_by_project,
    update_job_status,
)
from app.db.repositories.plans import get_user_plan_code
from app.db.repositories.projects import get_project
from app.domain.plan_rules import PlanEligibilityError, validate_job_creation_for_plan

router = APIRouter(tags=["jobs"])


@router.post(
    "/projects/{project_id}/jobs",
    response_model=JobResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_409_CONFLICT: {
            "model": JobCreateErrorResponse,
            "description": "Job creation rejected by plan limits.",
        }
    },
)
def create_job_endpoint(
    project_id: UUID,
    payload: JobCreateRequest,
    session: Session = Depends(get_db_session),
) -> JobResponse | JSONResponse:
    project = get_project(session=session, project_id=project_id)
    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found.")

    plan_code = get_user_plan_code(session=session, user_id=project.user_id)
    active_jobs_count = count_active_jobs_by_user(session=session, user_id=project.user_id)

    try:
        validate_job_creation_for_plan(
            plan_code=plan_code,
            requested_stems_count=len(payload.requested_stems),
            active_jobs_count=active_jobs_count,
        )
    except PlanEligibilityError as exc:
        error_payload = JobCreateErrorResponse(
            error=JobCreateErrorCode.PLAN_LIMIT_EXCEEDED,
            message=str(exc),
        )
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content=error_payload.model_dump(mode="json"),
        )

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


@router.patch("/jobs/{job_id}/status", response_model=JobResponse)
def update_job_status_endpoint(
    job_id: UUID,
    payload: JobStatusUpdateRequest,
    session: Session = Depends(get_db_session),
) -> JobResponse:
    job = get_job(session=session, job_id=job_id)
    if job is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found.")

    job = update_job_status(session=session, job=job, status=payload.status)
    return JobResponse.model_validate(job)
