from orion.core.auto.schemas import AutoAdminSchema


def list_admin_models() -> list[AutoAdminSchema]:
    import pkgutil
    from pathlib import Path

    from orion.core.users.database import User

    app_package_modules = pkgutil.iter_modules(
        [str(Path(__file__).parent.parent / "app")]
    )
    admin_models: list[AutoAdminSchema] = [
        AutoAdminSchema(model=User, icon="fa fa-user")
    ]
    for _ in app_package_modules:
        pass
    #     # Import all sqlalchemy models from the module
    #     mod = __import__(f"orion.app.admin.{module.name}.database", fromlist=["*"])
    #     for attr in dir(mod):
    #         model = getattr(mod, attr)
    #         if isinstance(model, type) and issubclass(model, Base):
    #             admin_models.append((model, None, None, None, None))
    return admin_models
