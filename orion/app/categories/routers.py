from fastapi import APIRouter, Depends, status

from .deps import category_service
from .schemas import Category
from .services import CategoryService

router = APIRouter(
    tags=["categories"],
)


@router.get(
    "/categories",
    response_model=list[Category],
    summary="List all categories",
    description="List all categories",
    response_description="List of categories",
    responses={
        status.HTTP_200_OK: {"description": "List of categories"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal Server Error"},
    },
)
async def list(
    service: CategoryService = Depends(category_service),
) -> list[Category]:
    return await service.list()
