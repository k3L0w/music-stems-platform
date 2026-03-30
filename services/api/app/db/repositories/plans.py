from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.models import Plan


def list_plans(session: Session) -> list[Plan]:
    statement = select(Plan).order_by(Plan.name.asc())
    return list(session.scalars(statement))
