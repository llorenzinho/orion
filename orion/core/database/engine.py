from functools import lru_cache

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from orion.core.enums import Environment, LogLevel
from orion.core.settings import get_settings


class Base(DeclarativeBase):
    pass


@lru_cache
def get_engine():
    cfg = get_settings()
    return create_async_engine(
        cfg.db.connection_string,
        echo=cfg.env is Environment.DEVELOPMENT and cfg.log.level == LogLevel.DEBUG,
    )


@lru_cache
def session_maker() -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(get_engine(), expire_on_commit=False)
