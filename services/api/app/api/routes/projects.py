from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.orm import Session

from app.api.schemas.projects import (
    ProjectCreateRequest,
    ProjectResponse,
    ProjectUpdateRequest,
)
from app.api.schemas.uploads import UploadCompleteRequest, UploadTargetResponse
from app.db.dependencies import get_db_session
from app.db.repositories.projects import (
    build_upload_target,
    confirm_project_upload,
    create_project,
    delete_project,
    get_project,
    list_projects,
    update_project,
)
from app.domain.models import User

router = APIRouter(prefix="/projects", tags=["projects"])


@router.get("", response_model=list[ProjectResponse])
def read_projects(
    user_id: UUID | None = Query(default=None),
    session: Session = Depends(get_db_session),
) -> list[ProjectResponse]:
    projects = list_projects(session=session, user_id=user_id)
    return [ProjectResponse.model_validate(project) for project in projects]


@router.get("/{project_id}", response_model=ProjectResponse)
def read_project(project_id: UUID, session: Session = Depends(get_db_session)) -> ProjectResponse:
    project = get_project(session=session, project_id=project_id)
    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found.")

    return ProjectResponse.model_validate(project)


@router.post("/{project_id}/upload-target", response_model=UploadTargetResponse)
def create_upload_target(
    project_id: UUID,
    session: Session = Depends(get_db_session),
) -> UploadTargetResponse:
    project = get_project(session=session, project_id=project_id)
    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found.")

    return UploadTargetResponse.model_validate(build_upload_target(project))


@router.post("/{project_id}/upload-complete", response_model=ProjectResponse)
def complete_project_upload(
    project_id: UUID,
    payload: UploadCompleteRequest,
    session: Session = Depends(get_db_session),
) -> ProjectResponse:
    project = get_project(session=session, project_id=project_id)
    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found.")

    project = confirm_project_upload(
        session=session,
        project=project,
        object_key=payload.object_key,
        source_filename=payload.source_filename,
        source_content_type=payload.source_content_type,
        source_size_bytes=payload.source_size_bytes,
    )
    return ProjectResponse.model_validate(project)


@router.post("", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
def create_project_endpoint(
    payload: ProjectCreateRequest,
    session: Session = Depends(get_db_session),
) -> ProjectResponse:
    user = session.get(User, payload.user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")

    project = create_project(session=session, data=payload.model_dump())
    return ProjectResponse.model_validate(project)


@router.patch("/{project_id}", response_model=ProjectResponse)
def update_project_endpoint(
    project_id: UUID,
    payload: ProjectUpdateRequest,
    session: Session = Depends(get_db_session),
) -> ProjectResponse:
    project = get_project(session=session, project_id=project_id)
    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found.")

    if not payload.model_dump(exclude_unset=True):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No fields provided for update.")

    if payload.user_id is not None:
        user = session.get(User, payload.user_id)
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")

    project = update_project(
        session=session,
        project=project,
        data=payload.model_dump(exclude_unset=True),
    )
    return ProjectResponse.model_validate(project)


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project_endpoint(project_id: UUID, session: Session = Depends(get_db_session)) -> Response:
    project = get_project(session=session, project_id=project_id)
    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found.")

    delete_project(session=session, project=project)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
