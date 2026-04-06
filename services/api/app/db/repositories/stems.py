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


def build_stem_download_target(stem: GeneratedStem) -> dict[str, object]:
    return {
        "stem_id": stem.id,
        "stem_type": stem.stem_type,
        "file_key": stem.file_key,
        "download_url": f"https://mock-storage.local/download/{stem.file_key}",
        "download_method": "GET",
        "expires_in_seconds": 3600,
    }


def list_project_download_targets(session: Session, project_id: UUID) -> list[dict[str, object]]:
    stems = list_stems_by_project(session=session, project_id=project_id)
    return [build_stem_download_target(stem) for stem in stems]
