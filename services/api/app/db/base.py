from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


from app.domain import models  # noqa: E402,F401
