from fastapi import FastAPI

from orion.core.enums import OpenapiTags
from orion.core.users.deps import fapi_users
from orion.core.users.schemas import UserCreate, UserRead, UserUpdate
from orion.core.users.services import jwt_backend


def configure_app_auth(app: FastAPI) -> FastAPI:

    auth_prefix = "/auth"

    app.include_router(
        fapi_users.get_auth_router(jwt_backend, requires_verification=False),
        prefix=auth_prefix,
        tags=[OpenapiTags.AUTH],
    )

    app.include_router(
        fapi_users.get_register_router(UserRead, UserCreate),
        prefix=auth_prefix,
        tags=[OpenapiTags.AUTH],
    )
    app.include_router(
        fapi_users.get_reset_password_router(),
        prefix=auth_prefix,
        tags=[OpenapiTags.AUTH],
    )
    app.include_router(
        fapi_users.get_verify_router(UserRead),
        prefix=auth_prefix,
        tags=[OpenapiTags.AUTH],
    )
    app.include_router(
        fapi_users.get_users_router(UserRead, UserUpdate),
        prefix="/users",
        tags=[OpenapiTags.USERS],
    )
    return app
