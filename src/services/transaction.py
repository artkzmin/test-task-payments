import hashlib
import hmac

from src.services.base import BaseService
from src.schemes import (
    Transaction,
    TransactionAddRequest,
    AccountAdd,
    TransactionAdd,
    AccountPatch,
)
from src.config import settings
from src.exceptions import (
    IncorrectTransactionException,
    TransactionAlreadyExistsException,
    TransactionNotFoundException,
    ObjectNotFoundException,
)
from src.services import AccountService


class TransactionService(BaseService):
    async def get_transactions_by_user_id(self, user_id: int) -> list[Transaction]:
        try:
            return await self.db.transaction.get_transaction_by_user_id(user_id=user_id)
        except ObjectNotFoundException as ex:
            raise TransactionNotFoundException from ex

    async def add_transaction(self, data: TransactionAddRequest) -> None:
        # Проверка подписи
        if not self.verify_transaction(data):
            raise IncorrectTransactionException
        if not await self.check_unique_transaction(data.transaction_id):
            raise TransactionAlreadyExistsException

        # Создание счета, если его не существует + пополнение
        account = await AccountService(self.db).get_one_or_none_account(data.account_id)
        if not account:
            await AccountService(self.db).add_account(
                AccountAdd(id=data.account_id, balance=data.amount, user_id=data.user_id)
            )
        elif account.user_id != data.user_id:
            raise IncorrectTransactionException
        else:
            await AccountService(self.db).partial_edit_account(
                data=AccountPatch(balance=account.balance + data.amount),
                id=data.account_id,
            )

        # Сохранение транзакции
        await self.db.transaction.add(
            TransactionAdd(account_id=data.account_id, id=data.transaction_id, amount=data.amount)
        )

        await self.db.commit()

    def verify_transaction(self, data: TransactionAddRequest) -> bool:
        expected_string = f"{int(data.account_id)}{int(data.amount)}{data.transaction_id}{int(data.user_id)}{settings.TRANSACTION_SECRET_KEY}"

        expected_signature = hashlib.sha256(expected_string.encode()).hexdigest()
        return hmac.compare_digest(expected_signature, data.signature)

    async def check_unique_transaction(self, id: str) -> bool:
        transaction = await self.db.transaction.get_one_or_none(id=id)
        if transaction:
            return False
        return True
