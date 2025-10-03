from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from functools import lru_cache

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from orion.core.database.engine import Base, get_engine, session_maker
from orion.core.exceptions import DatabaseConnectionError
from orion.core.log import get_logger


class Database:
    def __init__(self) -> None:
        self.log = get_logger(__name__)

    @property
    @asynccontextmanager
    async def session(self) -> AsyncGenerator[AsyncSession, None]:
        self.log.debug("Opening new database session")
        async with session_maker()() as s:
            yield s
        self.log.debug("Database session closed")

    async def ping(self):
        try:
            async with self.session as session:
                select_stmt = text("SELECT 1")
                result = session.execute(select_stmt)
                res = result
                self.log.debug(f"Database connection test successful: {res}")
        except Exception as e:
            self.log.error(f"Database connection test failed: {e}")
            raise DatabaseConnectionError("Failed to connect to the database") from e

    async def migrate(self):
        async with get_engine().begin() as conn:
            await conn.run_sync(Base.metadata.create_all)


@lru_cache
def get_database() -> Database:
    return Database()
