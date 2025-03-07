from fastapi import APIRouter
from src.schemes import AccountWithoutUserID
from src.api.dependencies import CommonUserIDDep, DBDep
from src.services import AccountService
from src.api.docs import DocsStrings
from src.exceptions import AccountAlreadyExistsException
from src.api.exceptions import AccountAlreadyExistsHTTPException


router = APIRouter(prefix="/account", tags=["Счёт"])


@router.get(
    "/me",
    summary="Получение всех счетов для текущего аутентифицированного пользователя",
    description=f"{DocsStrings.ABOUT_CURRENT_AUTH_USER}. {DocsStrings.JUST_COMMON_USER_ACCESS}",
)
async def get_me(user_id: CommonUserIDDep, db: DBDep) -> list[AccountWithoutUserID]:
    try:
        return await AccountService(db).get_accounts_without_user_id_by_user_id(user_id)
    except AccountAlreadyExistsException:
        raise AccountAlreadyExistsHTTPException
