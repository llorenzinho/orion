from fastapi import FastAPI


def configure_app(app: FastAPI) -> FastAPI:
    import pkgutil
    from pathlib import Path

    from orion.core.users.configure_app import configure_app_auth

    app_parent = Path(__file__).parent.parent.parent / "app"
    for module in pkgutil.iter_modules([str(app_parent)]):
        mod = __import__(f"orion.app.{module.name}.routers", fromlist=["*"])
        if hasattr(mod, "router"):
            app.include_router(getattr(mod, "router"), prefix=f"/api")

    configure_app_auth(app)
    return app
