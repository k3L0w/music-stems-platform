from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.models import User


def list_users(session: Session) -> list[User]:
    statement = select(User).order_by(User.display_name.asc(), User.email.asc())
    return list(session.scalars(statement))
