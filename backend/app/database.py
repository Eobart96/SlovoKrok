from collections.abc import Generator
from pathlib import Path

from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.config import get_settings


class Base(DeclarativeBase):
    pass


SQLITE_BUSY_TIMEOUT_MS = 5_000


def _connect_args(database_url: str) -> dict[str, object]:
    return {"check_same_thread": False, "timeout": SQLITE_BUSY_TIMEOUT_MS / 1_000} if database_url.startswith("sqlite") else {}


def _configure_sqlite_connection(dbapi_connection, _connection_record) -> None:
    cursor = dbapi_connection.cursor()
    try:
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.execute(f"PRAGMA busy_timeout={SQLITE_BUSY_TIMEOUT_MS}")
    finally:
        cursor.close()


def create_database_engine(database_url: str) -> Engine:
    database_engine = create_engine(database_url, connect_args=_connect_args(database_url))
    if database_url.startswith("sqlite"):
        event.listen(database_engine, "connect", _configure_sqlite_connection)
    return database_engine


settings = get_settings()
if settings.database_url.startswith("sqlite:///"):
    database_path = Path(settings.database_url.removeprefix("sqlite:///"))
    database_path.parent.mkdir(parents=True, exist_ok=True)

engine = create_database_engine(settings.database_url)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
