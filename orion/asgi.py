import logging.config
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI, status
from starlette.middleware.sessions import SessionMiddleware

from orion.core import constants
from orion.core.admin import mount_admin
from orion.core.apis import core_router_v1
from orion.core.enums import Environment, OpenapiTags
from orion.core.middlewares import RouterLoggingMiddleware
from orion.core.settings import get_settings
from orion.core.auto.routers import configure_app

logging.config.dictConfig(get_settings().log.uvicorn_log_config())


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    root_logger = logging.getLogger("root")
    root_logger.debug("ORION APP STARTING")
    root_logger.debug(f"{'Environment:'.ljust(18)} {get_settings().env}")
    root_logger.debug(f"{'Service Version:'.ljust(18)} {constants.APP_VERSION}")
    if get_settings().env is Environment.DEVELOPMENT:
        root_logger.warning(
            "Running in DEVELOPMENT mode. Do not use this in production!"
        )
        root_logger.debug("running database migrations...")
        from orion.core.database.db import get_database

        await get_database().migrate()
    yield
    root_logger.debug("ORION APP STOPPED")


app = FastAPI(
    title=get_settings().app_name,
    version=constants.APP_VERSION,
    lifespan=lifespan,
    debug=get_settings().env is Environment.DEVELOPMENT,
)

app.add_middleware(RouterLoggingMiddleware)
app.add_middleware(SessionMiddleware, secret_key=get_settings().session_secret)
mount_admin(app)

# Routers
configure_app(app)


@app.get("/healthz", tags=[OpenapiTags.SYSTEM], status_code=status.HTTP_204_NO_CONTENT)
def health_check():
    return None


app.include_router(core_router_v1, prefix="/api/v1")
