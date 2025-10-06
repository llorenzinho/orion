from fastapi import FastAPI


def configure_app(app: FastAPI) -> FastAPI:
    from pathlib import Path

    from orion.core.users.configure_app import configure_app_auth

    Path(__file__).parent.parent / "app"

    configure_app_auth(app)
    return app
