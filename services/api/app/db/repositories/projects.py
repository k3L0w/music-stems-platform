from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.enums import ProjectStatus
from app.domain.models import Project


def list_projects(session: Session, user_id: UUID | None = None) -> list[Project]:
    statement = select(Project).order_by(Project.created_at.desc())
    if user_id is not None:
        statement = statement.where(Project.user_id == user_id)

    return list(session.scalars(statement))


def get_project(session: Session, project_id: UUID) -> Project | None:
    return session.get(Project, project_id)


def create_project(session: Session, data: dict[str, object]) -> Project:
    project = Project(**data)
    session.add(project)
    session.commit()
    session.refresh(project)
    return project


def update_project(
    session: Session,
    project: Project,
    data: dict[str, object],
) -> Project:
    for field_name, value in data.items():
        setattr(project, field_name, value)

    session.add(project)
    session.commit()
    session.refresh(project)
    return project


def delete_project(session: Session, project: Project) -> None:
    session.delete(project)
    session.commit()


def build_upload_target(project: Project) -> dict[str, object]:
    object_key = f"projects/{project.id}/source/{project.source_filename}"
    upload_headers: dict[str, str] = {}
    if project.source_content_type is not None:
        upload_headers["content-type"] = project.source_content_type

    return {
        "project_id": project.id,
        "object_key": object_key,
        "upload_url": f"https://mock-storage.local/upload/{object_key}",
        "upload_method": "PUT",
        "upload_headers": upload_headers,
        "expires_in_seconds": 3600,
    }


def confirm_project_upload(
    session: Session,
    project: Project,
    *,
    object_key: str,
    source_filename: str | None,
    source_content_type: str | None,
    source_size_bytes: int | None,
) -> Project:
    project.source_object_key = object_key
    if source_filename is not None:
        project.source_filename = source_filename
    if source_content_type is not None:
        project.source_content_type = source_content_type
    if source_size_bytes is not None:
        project.source_size_bytes = source_size_bytes
    project.status = ProjectStatus.UPLOADED

    session.add(project)
    session.commit()
    session.refresh(project)
    return project
