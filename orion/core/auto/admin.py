import inspect
from orion.core.auto.schemas import AutoAdminSchema
from orion.core.database.engine import Base


def list_admin_models() -> list[AutoAdminSchema]:
    import pkgutil
    from pathlib import Path

    from orion.core.users.database import User

    app_package_modules = pkgutil.iter_modules(
        [str(Path(__file__).parent.parent.parent / "app")]
    )
    admin_models: list[AutoAdminSchema] = [
        AutoAdminSchema(model=User, icon="fa fa-user")
    ]
    for module in app_package_modules:
        mod = __import__(f"orion.app.{module.name}.database", fromlist=["*"])
        for attr in dir(mod):
            model = getattr(mod, attr)
            if inspect.isclass(model) and issubclass(model, Base):
                print("MODEL", model)
                admin_models.append(
                    AutoAdminSchema(
                        model=model,
                        icon=getattr(mod, "ADMIN_ICON", None),
                        label=getattr(mod, "ADMIN_LABEL", None),
                        identity=getattr(mod, "ADMIN_IDENTITY", None)
                    )
                )
    return admin_models
