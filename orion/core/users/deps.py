import uuid
from collections.abc import AsyncGenerator

from fastapi import Depends
from fastapi_users import FastAPIUsers
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase

from orion.core.database.db import Database
from orion.core.database.deps import database
from orion.core.users.database import User
from orion.core.users.service import UserManager, jwt_backend


async def user_db(
    db: Database = Depends(database),
) -> AsyncGenerator[SQLAlchemyUserDatabase, None]:
    async with db.session as session:
        yield SQLAlchemyUserDatabase(session, User)


async def get_user_manager(user_db: SQLAlchemyUserDatabase = Depends(user_db)):
    yield UserManager(user_db)


fapi_users = FastAPIUsers[User, uuid.UUID](get_user_manager, [jwt_backend])
auth_user = fapi_users.current_user(active=True)
