import logging
from functools import lru_cache

import pythonjsonlogger.jsonlogger as jsonlogger

from orion.core.constants import APP_VERSION
from orion.core.settings import get_settings


class VersionFilter(logging.Filter):
    def filter(self, record):
        record.version = APP_VERSION
        return True


@lru_cache()
def get_logger(name: str = __name__) -> logging.Logger:
    cfg = get_settings()
    logger = logging.getLogger(name)
    logger.setLevel(cfg.log.level.value)
    if not logger.handlers:
        console_handler = logging.StreamHandler()
        formatter = jsonlogger.JsonFormatter(  # type: ignore (actually exported from python-json-logger)
            fmt="%(asctime)s %(levelname)s %(name)s %(message)s %(version)s"
        )
        console_handler.setFormatter(formatter)
        console_handler.addFilter(VersionFilter())
        logger.addHandler(console_handler)
    logger.propagate = False
    return logger


app_logger = get_logger()
