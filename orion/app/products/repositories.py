from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from orion.core.log import get_logger
from .database import Product


class ProductRepo:
    def __init__(self, db: AsyncSession):
        self.__db = db
        self.__log = get_logger(self.__class__.__name__)

    @property
    def log(self):
        return self.__log

    @property
    def db(self) -> AsyncSession:
        return self.__db

    async def list(self) -> list[Product]:
        async with self.db as session:
            statement = select(Product)
            result = await session.execute(statement)
            return list(result.scalars().all())

    async def get(self, product_id: int) -> Product | None:
        async with self.db as session:
            statement = select(Product).where(Product.id == product_id)
            result = await session.execute(statement)
            return result.scalars().first()
