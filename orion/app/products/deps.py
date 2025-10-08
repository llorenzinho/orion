from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from orion.core.database.deps import database
from .repositories import ProductRepo
from .services import ProductService


def product_repo(db: AsyncSession = Depends(database)) -> ProductRepo:
    return ProductRepo(db)


def product_service(repo: ProductRepo = Depends(product_repo)) -> ProductService:
    return ProductService(repo)
