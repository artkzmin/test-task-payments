from typing import Annotated

from fastapi import Depends, Request


from src.services import AuthService, UserService
from src.utils.db_manager import DBManager
from src.database import async_session_maker
from src.api.exceptions import (
    UserNotFoundHTTPException,
    NoAccessTokenHTTPException,
    IncorrectTokenHTTPException,
    UserNotCommonHTTPException,
    UserNotAdminHTTPException,
    TokenExpiredHTTPException,
)
from src.exceptions import (
    IncorrectTokenException,
    TokenExpiredException,
    UserNotFoundException,
)
from src.schemes import UserRoleEnum


def get_db_manager():
    return DBManager(session_factory=async_session_maker)


async def get_db():
    async with get_db_manager() as db:
        yield db


DBDep = Annotated[DBManager, Depends(get_db)]


def get_token(request: Request) -> str:
    token = request.cookies.get("access_token")
    if not token:
        raise NoAccessTokenHTTPException
    return token


async def get_current_user_id(db: DBDep, token: str = Depends(get_token)) -> int:
    try:
        data = AuthService().decode_token(token)
    except IncorrectTokenException:
        raise IncorrectTokenHTTPException
    except TokenExpiredException:
        raise TokenExpiredHTTPException
    user_id = data.get("user_id")
    if not user_id:
        raise UserNotFoundHTTPException
    try:
        await UserService(db).get_user(user_id)
    except UserNotFoundException:
        raise UserNotFoundHTTPException
    return user_id


UserIDDep = Annotated[int, Depends(get_current_user_id)]


async def get_current_common_user_id(db: DBDep, user_id: UserIDDep) -> int:
    if await UserService(db).check_user_role(id=user_id, role=UserRoleEnum.COMMON):
        return user_id
    raise UserNotCommonHTTPException


CommonUserIDDep = Annotated[int, Depends(get_current_common_user_id)]


async def get_current_admin_id(db: DBDep, user_id: UserIDDep) -> int:
    if await UserService(db).check_user_role(id=user_id, role=UserRoleEnum.ADMIN):
        return user_id
    raise UserNotAdminHTTPException


AdminIDDep = Annotated[int, Depends(get_current_admin_id)]
