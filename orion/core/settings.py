from functools import lru_cache

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

from orion.core.enums import Environment, LogLevel


class JwtConfig(BaseModel):
    secret: str = ""
    lifetime_seconds: int = 3600


class LogConfig(BaseModel):
    level: LogLevel = LogLevel.INFO
    format: str = "[%(asctime)s] [%(levelname)s] [%(name)s] | %(message)s"
    datefmt: str = "%Y-%m-%d %H:%M:%S"

    def uvicorn_log_config(self) -> dict:
        return {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "default": {
                    "format": self.format,
                    "datefmt": self.datefmt,
                },
            },
            "handlers": {
                "default": {
                    "class": "logging.StreamHandler",
                    "formatter": "default",
                },
            },
            "root": {
                "handlers": ["default"],
                "level": self.level.value,
            },
            "loggers": {
                "uvicorn": {
                    "handlers": ["default"],
                    "level": self.level.value,
                    "propagate": False,
                },
                "uvicorn.error": {
                    "handlers": ["default"],
                    "level": LogLevel.WARNING.value,
                    "propagate": False,
                },
                "uvicorn.access": {
                    "handlers": [],
                    "level": self.level.value,
                    "propagate": False,
                },
            },
        }


class DatabaseConfig(BaseModel):
    connection_string: str


class ServerConfig(BaseModel):
    host: str = "localhost"
    port: int = 8000


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        env_prefix="ORION_",
        env_nested_delimiter="__",
    )

    app_name: str = "Orion"
    env: Environment = Environment.PRODUCTION
    session_secret: str
    log: LogConfig
    server: ServerConfig
    db: DatabaseConfig
    jwt: JwtConfig


@lru_cache
def get_settings() -> AppSettings:
    return AppSettings()  # type: ignore
