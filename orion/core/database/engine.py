from functools import lru_cache

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from orion.core.enums import Environment, LogLevel
from orion.core.settings import get_settings


@lru_cache
def get_engine():
    cfg = get_settings()
    return create_engine(
        cfg.db.connection_string,
        echo=cfg.env is Environment.DEVELOPMENT and cfg.log.level == LogLevel.DEBUG,
    )


def get_session_maker():
    async_session_maker = sessionmaker(
        get_engine(), class_=AsyncSession, expire_on_commit=False
    )
    return async_session_maker
