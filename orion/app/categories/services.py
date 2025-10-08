from orion.core.log import get_logger
from .repositories import CategoryRepo
from .schemas import Category


class CategoryService:
    def __init__(self, repo: CategoryRepo):
        self.repo = repo
        self.__log = get_logger(self.__class__.__name__)

    @property
    def log(self):
        return self.__log

    async def get(self, category_id: int) -> Category | None:
        ret = await self.repo.get(category_id)
        if not ret:
            return None
        return Category.model_validate(ret.__dict__)

    async def list(self) -> list[Category]:
        data = await self.repo.list()
        return [Category.model_validate(item.__dict__) for item in data]
