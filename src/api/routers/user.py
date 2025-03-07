from fastapi import APIRouter, Body, Path
from typing import Final
from src.schemes import (
    UserAddRequest,
    UserPatchRequest,
    UserWithReals,
    UserWithFullName,
)
from src.api.schemes import StatusOK, ID
from src.services import UserService, AuthService
from src.api.dependencies import DBDep, UserIDDep, AdminIDDep
from src.exceptions import UserNotFoundException, UserAlreadyExistsException
from src.api.exceptions import (
    UserNotFoundHTTPException,
    UserAlreadyExistsHTTPException,
    CommonUserNotFoundHTTPException,
)
from src.api.utils import check_user_exists
from src.api.docs import DocsStrings, DocsExamples

TAG: Final = "Пользователи"
router = APIRouter(prefix="/user", tags=[TAG])
users_router = APIRouter(prefix="/users", tags=[TAG])


@router.get(
    "/me",
    summary="Получение данных о текущем аутентифицированном пользователе",
    description=DocsStrings.ABOUT_CURRENT_AUTH_USER,
)
async def get_me(db: DBDep, user_id: UserIDDep) -> UserWithFullName:
    try:
        return await UserService(db).get_user_with_full_name(id=user_id)
    except UserNotFoundException:
        raise UserNotFoundHTTPException


@router.post(
    "/",
    summary="Регистрация нового пользователя",
    description=DocsStrings.JUST_ADMIN_USER_ACCESS,
)
async def create_user(
    db: DBDep,
    admin_id: AdminIDDep,
    user_data: UserAddRequest = Body(openapi_examples=DocsExamples.USER_EXAMPLES),
) -> ID:
    try:
        user = await AuthService(db).register_user(user_data)
    except UserAlreadyExistsException:
        raise UserAlreadyExistsHTTPException
    return ID(id=user.id)


@router.delete(
    "/{user_id}",
    summary="Удаление пользователя",
    description=DocsStrings.JUST_ADMIN_USER_ACCESS,
)
async def delete_user(
    db: DBDep,
    admin_id: AdminIDDep,
    user_id: int = Path(
        ...,
        title=DocsStrings.USER_ID_TITLE,
        description=DocsStrings.USER_ID_DESCRIPTION,
    ),
) -> StatusOK:
    await check_user_exists(db, user_id)
    await UserService(db).delete_user(user_id)
    return StatusOK


@router.put(
    "/{user_id}",
    summary="Изменение данных пользователя",
    description=f"PUT-запрос, необходимо предоставить все данные о пользователе. {DocsStrings.JUST_ADMIN_USER_ACCESS}",
)
async def edit_user(
    db: DBDep,
    admin_id: AdminIDDep,
    user_id: int = Path(
        ...,
        title=DocsStrings.USER_ID_TITLE,
        description=DocsStrings.USER_ID_DESCRIPTION,
    ),
    user_data: UserAddRequest = Body(openapi_examples=DocsExamples.USER_EXAMPLES),
) -> StatusOK:
    await check_user_exists(db, user_id)
    await UserService(db).edit_user(id=user_id, data=user_data)
    return StatusOK


@router.patch(
    "/{user_id}",
    summary="Частичное изменение пользователя",
    description=f"PATCH-запрос, необходимо указать только те данные пользователя, которые нужно изменить. {DocsStrings.JUST_ADMIN_USER_ACCESS}",
)
async def partial_edit_user(
    db: DBDep,
    admin_id: AdminIDDep,
    user_id: int = Path(
        ...,
        title=DocsStrings.USER_ID_TITLE,
        description=DocsStrings.USER_ID_DESCRIPTION,
    ),
    user_data: UserPatchRequest = Body(openapi_examples=DocsExamples.USER_EXAMPLES),
) -> StatusOK:
    await check_user_exists(db, user_id)
    await UserService(db).partial_edit_user(id=user_id, data=user_data)
    return StatusOK


@router.get(
    "/{user_id}",
    summary="Получение пользователя",
    description=DocsStrings.JUST_ADMIN_USER_ACCESS,
)
async def get_user(
    db: DBDep,
    admin_id: AdminIDDep,
    user_id: int = Path(
        ...,
        title=DocsStrings.USER_ID_TITLE,
        description=DocsStrings.USER_ID_DESCRIPTION,
    ),
) -> UserWithReals:
    try:
        return await UserService(db).get_user_with_accounts(user_id)
    except UserNotFoundException:
        raise CommonUserNotFoundHTTPException


@users_router.get(
    "",
    summary="Получение всех пользователей",
    description=DocsStrings.JUST_ADMIN_USER_ACCESS,
)
async def get_all_users(db: DBDep, admin_id: AdminIDDep) -> list[UserWithReals]:
    return await UserService(db).get_all_common_users_with_accounts()
