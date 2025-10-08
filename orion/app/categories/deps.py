from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from orion.core.database.deps import database
from .repositories import CategoryRepo
from .services import CategoryService


def category_repo(db: AsyncSession = Depends(database)) -> CategoryRepo:
    return CategoryRepo(db)


def category_service(repo: CategoryRepo = Depends(category_repo)) -> CategoryService:
    return CategoryService(repo)
