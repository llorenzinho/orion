from orion.core.database.engine import Base


def list_admin_models() -> (
    list[tuple[type[Base], str | None, str | None, str | None, str | None]]
):
    import pkgutil
    from pathlib import Path

    from orion.core.database.engine import Base
    from orion.core.users.database import User

    app_package_modules = pkgutil.iter_modules(
        [str(Path(__file__).parent.parent / "app")]
    )
    admin_models: list[
        tuple[type[Base], str | None, str | None, str | None, str | None]
    ] = [(User, None, "fa fa-user", None, None)]
    for _ in app_package_modules:
        pass
    #     # Import all sqlalchemy models from the module
    #     mod = __import__(f"orion.app.{module.name}.database", fromlist=["*"])
    #     for attr in dir(mod):
    #         model = getattr(mod, attr)
    #         if isinstance(model, type) and issubclass(model, Base):
    #             admin_models.append((model, None, None, None, None))
    return admin_models
