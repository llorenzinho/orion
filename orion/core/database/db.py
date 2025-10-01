from contextlib import contextmanager
from functools import lru_cache

from sqlmodel import Session, SQLModel, text

from orion.core.database.engine import get_engine
from orion.core.exceptions import DatabaseConnectionError
from orion.core.log import get_logger


class Database:
    def __init__(self) -> None:
        self.log = get_logger(__name__)

    @property
    @contextmanager
    def session(self):
        self.log.debug("Opening new database session")
        with Session(get_engine()) as session:
            yield session
        self.log.debug("Database session closed")

    def ping(self):
        try:
            with self.session as session:
                select_stmt = text("SELECT 1")
                result = session.exec(select_stmt)  # type: ignore
                res = result.scalar()
                self.log.debug(f"Database connection test successful: {res}")
        except Exception as e:
            self.log.error(f"Database connection test failed: {e}")
            raise DatabaseConnectionError("Failed to connect to the database") from e

    def migrate(self):
        SQLModel.metadata.create_all(get_engine())


@lru_cache
def get_database() -> Database:
    return Database()
