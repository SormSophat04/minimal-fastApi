from app.db.base import Base
from app.db.session import engine


def init_db() -> None:
    # import models so metadata is registered
    from app.models import user  # noqa: F401

    Base.metadata.create_all(bind=engine)
