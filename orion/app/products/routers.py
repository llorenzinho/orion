from fastapi import APIRouter, Depends, HTTPException, status

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
    },
)
async def list_all(
    service: ProductService = Depends(product_service),
) -> list[Product]:
    return await service.list_all()


@router.get(
    "/products/{product_id:int}",
    response_model=Product,
    summary="Get a product by ID",
    description="Get a product by its ID",
    response_description="The product with the given ID",
    responses={
        status.HTTP_200_OK: {"description": "The product with the given ID"},
        status.HTTP_404_NOT_FOUND: {"description": "Product not found"},
    },
)
async def get(
    product_id: int,
    service: ProductService = Depends(product_service),
) -> Product | None:
    data = await service.get(product_id)
    if not data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )
    return data


@router.get(
    "/products/category/{category_id:int}",
    response_model=list[Product],
    summary="Get products by category ID",
    description="Get all products that belong to a specific category by its ID",
    response_description="List of products in the specified category",
    responses={
        status.HTTP_200_OK: {
            "description": "List of products in the specified category"
        },
    },
)
async def get_by_category(
    category_id: int,
    service: ProductService = Depends(product_service),
) -> list[Product]:
    data = await service.get_by_category(category_id)
    return data
