from src.services import UserService
from src.exceptions import UserNotFoundException
from src.api.exceptions import UserNotFoundHTTPException
from src.api.dependencies import DBDep


async def check_user_exists(db: DBDep, id: int) -> None:
    try:
        await UserService(db).check_user_exists(id)
    except UserNotFoundException:
        raise UserNotFoundHTTPException
