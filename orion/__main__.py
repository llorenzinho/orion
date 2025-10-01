import uvicorn

from orion.core.enums import Environment
from orion.core.settings import get_settings

if __name__ == "__main__":
    settings = get_settings()
    uvicorn.run(
        "orion.app:app",
        host=settings.server.host,
        port=settings.server.port,
        reload=settings.env is Environment.DEVELOPMENT,
    )
