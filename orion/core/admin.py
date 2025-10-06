from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from starlette.requests import Request
from starlette.responses import Response
from starlette_admin.auth import AdminConfig, AdminUser, AuthProvider
from starlette_admin.contrib.sqla import Admin, ModelView

from orion.core.auto.admin import list_admin_models
from orion.core.database.db import get_database
from orion.core.database.engine import get_engine
from orion.core.users.database import User
from orion.core.users.services import UserManager, get_jwt_strategy


class FastAPIUsersAuth(AuthProvider):

    async def login(
        self,
        username: str,
        password: str,
        remember_me: bool,
        request: Request,
        response: Response,
    ) -> Response:
        async with get_database().session as session:
            user_db = SQLAlchemyUserDatabase(session, User)
            user_manager = UserManager(user_db)
            strategy = get_jwt_strategy()
            user = await user_manager.authenticate(
                OAuth2PasswordRequestForm(username=username, password=password)
            )
            if user is None or not user.is_active:
                raise HTTPException(status_code=400, detail="Invalid credentials")
            if not user.is_superuser:
                raise HTTPException(status_code=403, detail="User is not an admin")
            token = await strategy.write_token(user)
            request.session.update({"session": token})
            if remember_me:
                max_age = 60 * 60 * 24 * 30
                response.set_cookie(
                    key="session",
                    value=token,
                    max_age=max_age,
                    httponly=True,
                    secure=False,
                )
            return response

    async def is_authenticated(self, request) -> bool:
        token = request.session.get("session", None)
        if not token:
            return False
        async with get_database().session as session:
            user_db = SQLAlchemyUserDatabase(session, User)
            user_manager = UserManager(user_db)
            strategy = get_jwt_strategy()
            user: User = await strategy.read_token(token, user_manager)  # type: ignore
            if user and user.is_active and user.is_superuser:
                return True
            return False

    def get_admin_config(self, request: Request) -> AdminConfig:
        # Update app title according to current_user
        # Update logo url according to current_user
        # if user.get("company_logo_url", None):
        #     custom_logo_url = request.url_for("static", path=user["company_logo_url"])
        return AdminConfig(
            app_title="admin",
            # logo_url=custom_logo_url,
        )

    def get_admin_user(self, request: Request) -> AdminUser:
        # photo_url = None
        # if user["avatar"] is not None:
        #     photo_url = request.url_for("static", path=user["avatar"])
        return AdminUser(
            username="admin",
            # photo_url=photo_url,
        )

    async def logout(self, request: Request, response: Response) -> Response:
        request.session.clear()
        response.delete_cookie("session")
        return response


def mount_admin(app: FastAPI) -> FastAPI:
    admin = Admin(get_engine(), title="Orion Admin", auth_provider=FastAPIUsersAuth())

    # Create all tables in the database which are defined by Base's subclasses
    for m, name, icon, label, identity in list_admin_models():
        admin.add_view(
            ModelView(
                m,
                name=name if name else m.__name__,
                icon=icon,
                label=label,
                identity=identity,
            )
        )
    admin.mount_to(app)

    return app
