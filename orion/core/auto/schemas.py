from pydantic import BaseModel

from orion.core.database.engine import Base


class AutoAdminSchema(BaseModel):
    model: type[Base]
    name: str | None = None
    icon: str | None = None
    label: str | None = None
    identity: str | None = None
