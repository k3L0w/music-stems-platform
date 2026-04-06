from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.schemas.stems import StemDownloadTargetResponse, StemResponse
from app.db.dependencies import get_db_session
from app.db.repositories.projects import get_project
from app.db.repositories.stems import (
    build_stem_download_target,
    get_stem,
    list_project_download_targets,
    list_stems_by_project,
)

router = APIRouter(tags=["stems"])


@router.get("/projects/{project_id}/stems", response_model=list[StemResponse])
def read_project_stems(
    project_id: UUID,
    session: Session = Depends(get_db_session),
) -> list[StemResponse]:
    project = get_project(session=session, project_id=project_id)
    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found.")

    stems = list_stems_by_project(session=session, project_id=project.id)
    return [StemResponse.model_validate(stem) for stem in stems]


@router.get("/stems/{stem_id}", response_model=StemResponse)
def read_stem(stem_id: UUID, session: Session = Depends(get_db_session)) -> StemResponse:
    stem = get_stem(session=session, stem_id=stem_id)
    if stem is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Stem not found.")

    return StemResponse.model_validate(stem)


@router.post("/stems/{stem_id}/download-target", response_model=StemDownloadTargetResponse)
def create_stem_download_target(
    stem_id: UUID,
    session: Session = Depends(get_db_session),
) -> StemDownloadTargetResponse:
    stem = get_stem(session=session, stem_id=stem_id)
    if stem is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Stem not found.")

    return StemDownloadTargetResponse.model_validate(build_stem_download_target(stem))


@router.get(
    "/projects/{project_id}/download-targets",
    response_model=list[StemDownloadTargetResponse],
)
def read_project_download_targets(
    project_id: UUID,
    session: Session = Depends(get_db_session),
) -> list[StemDownloadTargetResponse]:
    project = get_project(session=session, project_id=project_id)
    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found.")

    download_targets = list_project_download_targets(session=session, project_id=project.id)
    return [StemDownloadTargetResponse.model_validate(target) for target in download_targets]
