from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from orion.core.log import get_logger
from .database import Category


class CategoryRepo:
    def __init__(self, db: AsyncSession):
        self.__db = db
        self.__log = get_logger(self.__class__.__name__)

    @property
    def log(self):
        return self.__log

    @property
    def db(self) -> AsyncSession:
        return self.__db

    async def list(self) -> list[Category]:
        async with self.db as session:
            statement = select(Category)
            result = await session.execute(statement)
            return list(result.scalars().all())

    async def get(self, category_id: int) -> Category | None:
        async with self.db as session:
            statement = select(Category).where(Category.id == category_id)
            result = await session.execute(statement)
            return result.scalars().first()
