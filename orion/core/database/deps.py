from collections.abc import AsyncGenerator

from orion.core.database.db import Database, get_database


async def database() -> AsyncGenerator[Database, None]:
    yield get_database()  # cached instance of Database class
