from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.models import GeneratedStem


def list_stems_by_project(session: Session, project_id: UUID) -> list[GeneratedStem]:
    statement = (
        select(GeneratedStem)
        .where(GeneratedStem.project_id == project_id)
        .order_by(GeneratedStem.created_at.desc())
    )
    return list(session.scalars(statement))


def get_stem(session: Session, stem_id: UUID) -> GeneratedStem | None:
    return session.get(GeneratedStem, stem_id)
