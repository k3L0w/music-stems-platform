from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

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
