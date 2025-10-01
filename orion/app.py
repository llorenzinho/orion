import logging.config
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI, status

from orion.core import constants
from orion.core.apis import core_router_v1
from orion.core.enums import Environment, OpenapiTags
from orion.core.middlewares import RouterLoggingMiddleware
from orion.core.settings import get_settings

logging.config.dictConfig(get_settings().log.uvicorn_log_config())


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    logging.getLogger("root").info("ORION APP STARTING")
    logging.getLogger("root").info(f"{'Environment:'.ljust(18)} {get_settings().env}")
    logging.getLogger("root").info(
        f"{'Service Version:'.ljust(18)} {constants.APP_VERSION}"
    )
    if get_settings().env is Environment.DEVELOPMENT:
        logging.getLogger("root").warning(
            "Running in DEVELOPMENT mode. Do not use this in production!"
        )
        logging.getLogger("root").info("running database migrations...")
        from orion.core.database.db import get_database

        get_database().migrate()
    yield
    logging.getLogger("root").info("ORION APP STOPPED")


app = FastAPI(
    lifespan=lifespan,
)


app.add_middleware(RouterLoggingMiddleware)


@app.get("/healthz", tags=[OpenapiTags.SYSTEM], status_code=status.HTTP_200_OK)
def health_check():
    return get_settings().db.connection_string


app.include_router(core_router_v1, prefix="/api/v1")
