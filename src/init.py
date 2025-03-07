import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))


import asyncio
from src.schemes import UserAddRequest, AccountAdd
from src.services import AuthService, AccountService
from src.database import async_session_maker, engine, BaseOrm
from src.utils.db_manager import DBManager
from src.config import settings
from src.schemes import UserRoleEnum
from src.exceptions import UserAlreadyExistsException, AccountAlreadyExistsException


async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(BaseOrm.metadata.drop_all)
        await conn.run_sync(BaseOrm.metadata.create_all)


async def init() -> None:
    async with DBManager(session_factory=async_session_maker) as db:
        admin = UserAddRequest(
            email=settings.ADMIN_EMAIL,
            role=UserRoleEnum.ADMIN,
            name=settings.ADMIN_NAME,
            surname=settings.ADMIN_SURNAME,
            patronymic=settings.ADMIN_PATRONYMIC,
            password=settings.ADMIN_PASSWORD,
        )
        common_user = UserAddRequest(
            email=settings.COMMON_EMAIL,
            role=UserRoleEnum.COMMON,
            name=settings.COMMON_NAME,
            surname=settings.COMMON_SURNAME,
            patronymic=settings.COMMON_PATRONYMIC,
            password=settings.COMMON_PASSWORD,
        )
        try:
            common_user = await AuthService(db).register_user(common_user)
        except UserAlreadyExistsException:
            pass

        try:
            admin = await AuthService(db).register_user(admin)
        except UserAlreadyExistsException:
            pass

        account = AccountAdd(id=1, balance=0, user_id=common_user.id)
        try:
            account = await AccountService(db).add_account_with_commit(account)
        except AccountAlreadyExistsException:
            pass


def main() -> None:
    asyncio.run(init())


if __name__ == "__main__":
    main()
