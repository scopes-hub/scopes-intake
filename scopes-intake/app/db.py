import os

from sqlalchemy import create_engine
from sqlalchemy.engine.url import make_url
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/app.db")


def _sqlite_connect_args(url: str) -> dict:
    if url.startswith("sqlite"):
        return {"check_same_thread": False}
    return {}


engine = create_engine(DATABASE_URL, connect_args=_sqlite_connect_args(DATABASE_URL), future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


def _ensure_sqlite_dir() -> None:
    url = make_url(DATABASE_URL)
    if not url.drivername.startswith("sqlite"):
        return
    if not url.database or url.database == ":memory:":
        return
    directory = os.path.dirname(url.database)
    if directory:
        os.makedirs(directory, exist_ok=True)


def init_db() -> None:
    from app import models

    _ensure_sqlite_dir()
    models.Base.metadata.create_all(bind=engine)


def get_session():
    with SessionLocal() as session:
        yield session
