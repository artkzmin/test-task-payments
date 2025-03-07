from src.services.base import BaseService
from src.schemes import Account, AccountAdd, AccountPatch, AccountWithoutUserID
from src.exceptions import ObjectNotFoundException, AccountNotFoundException


# В методах не вызывается commit, так как изменение/создание account происходит через transaction
class AccountService(BaseService):
    async def get_account_without_user_id(self, id: int) -> AccountWithoutUserID:
        try:
            account = await self.get_account(id)
        except AccountNotFoundException as ex:
            raise ex
        return AccountWithoutUserID(**account.model_dump())

    async def get_accounts_without_user_id_by_user_id(
        self, user_id: int
    ) -> list[AccountWithoutUserID]:
        accounts = await self.db.account.get_filtered(user_id=user_id)
        return [AccountWithoutUserID(**a.model_dump()) for a in accounts]

    async def get_one_or_none_account(self, id: int) -> Account | None:
        return await self.db.account.get_one_or_none(id=id)

    async def get_account(self, id: int) -> Account:
        try:
            return await self.db.account.get_one(id=id)
        except ObjectNotFoundException as ex:
            raise AccountNotFoundException from ex

    async def add_account(self, data: AccountAdd) -> Account:
        return await self.db.account.add(data)

    async def add_account_with_commit(self, data: AccountAdd) -> Account:
        account = await self.add_account(data)
        await self.db.commit()
        return account

    async def partial_edit_account(self, data: AccountPatch, id: int) -> None:
        await self.db.account.edit(data=data, exclude_unset=True, id=id)
