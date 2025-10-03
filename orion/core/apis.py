from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from orion.core.database.deps import Database, database
from orion.core.enums import OpenapiTags
from orion.core.exceptions import DatabaseConnectionError
from orion.core.schemas.db import DBConnectionTestResult
from orion.core.schemas.test import TestResultSchema

core_router_v1 = APIRouter(
    prefix="/system",
    tags=[OpenapiTags.SYSTEM],
)


@core_router_v1.get(
    "/check",
    response_model=TestResultSchema,
    status_code=status.HTTP_200_OK,
    summary="Check system connections",
    description="Check the health of system connections such as the database.",
    responses={
        status.HTTP_200_OK: {"description": "All connections are healthy"},
        status.HTTP_503_SERVICE_UNAVAILABLE: {
            "description": "One or more connections are unhealthy"
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Some unexpected error occurred"
        },
    },
)
async def check_connections(
    db: Database = Depends(database),
) -> JSONResponse:
    unavailable = False
    db_health = DBConnectionTestResult(
        success=True,
        message="up",
    )

    try:
        await db.ping()
    except DatabaseConnectionError as e:
        unavailable = True
        db_health.success = False
        db_health.message = str(e)

    return JSONResponse(
        status_code=(
            status.HTTP_503_SERVICE_UNAVAILABLE if unavailable else status.HTTP_200_OK
        ),
        content=TestResultSchema(db=db_health).model_dump(),
    )
