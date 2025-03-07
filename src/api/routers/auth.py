from fastapi import APIRouter, Response
from src.schemes import UserAuthRequest
from src.api.schemes import StatusOK, AccessToken
from src.api.dependencies import DBDep, UserIDDep
from src.exceptions import UserNotRegisteredException, IncorrectPasswordException
from src.api.exceptions import (
    UserNotRegisteredHTTPException,
    IncorrectPasswordHTTPException,
)
from src.services import AuthService


router = APIRouter(prefix="/auth", tags=["Аутентификация"])


@router.post(
    "/login",
    summary="Аутентификация пользователя",
    description="В случае успешной аутентификации добавляет токен доступа **access_token** в cookies",
)
async def login(db: DBDep, data: UserAuthRequest, response: Response) -> AccessToken:
    try:
        access_token = await AuthService(db).login_user(data)
    except UserNotRegisteredException:
        raise UserNotRegisteredHTTPException
    except IncorrectPasswordException:
        raise IncorrectPasswordHTTPException

    response.set_cookie("access_token", access_token)
    return AccessToken(access_token=access_token)


@router.post(
    "/logout",
    summary="Выход пользователя из системы",
    description="Удаляет токен доступа **access_token** из cookies",
)
async def logout(user_id: UserIDDep, response: Response) -> StatusOK:
    response.delete_cookie("access_token")
    return StatusOK
