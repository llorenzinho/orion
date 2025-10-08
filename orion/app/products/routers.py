from fastapi import APIRouter, Depends, status

from .deps import product_service
from .schemas import Product
from .services import ProductService

router = APIRouter(
    tags=["products"],
)


@router.get(
    "/products",
    response_model=list[Product],
    summary="List all products",
    description="List all products",
    response_description="List of products",
    responses={
        status.HTTP_200_OK: {"description": "List of products"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal Server Error"},
    },
)
async def list(
    service: ProductService = Depends(product_service),
) -> list[Product]:
    return await service.list()
