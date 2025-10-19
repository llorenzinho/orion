from orion.core.log import get_logger
from .repositories import ProductRepo
from .schemas import Product


class ProductService:
    def __init__(self, repo: ProductRepo):
        self.repo = repo
        self.__log = get_logger(self.__class__.__name__)

    @property
    def log(self):
        return self.__log

    async def get(self, product_id: int) -> Product | None:
        ret = await self.repo.get(product_id)
        if not ret:
            return None
        return Product.model_validate(ret.__dict__)

    async def list_all(self) -> list[Product]:
        data = await self.repo.list_all()
        return [Product.model_validate(item.__dict__) for item in data]

    async def get_by_category(self, category_id: int) -> list[Product]:
        data = await self.repo.get_by_category(category_id)
        return [Product.model_validate(item.__dict__) for item in data]
