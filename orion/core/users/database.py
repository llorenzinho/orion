from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID

from orion.core.database.engine import Base


class User(SQLAlchemyBaseUserTableUUID, Base):
    pass
