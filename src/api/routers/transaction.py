from fastapi import APIRouter, Body
from src.schemes import Transaction
from src.api.schemes import StatusOK
from src.api.dependencies import DBDep, CommonUserIDDep
from src.schemes import TransactionAddRequest
from src.services import TransactionService
from src.exceptions import (
    IncorrectTransactionException,
    TransactionAlreadyExistsException,
)
from src.api.exceptions import (
    IncorrectTransactionHTTPException,
    NotUniqueTransactionHTTPException,
)
from src.api.docs import DocsStrings, DocsExamples


router = APIRouter(prefix="/transaction", tags=["Платеж"])


@router.get(
    "/me",
    summary="Получение всех платежей для текущего аутентифицированного пользователя",
    description=f"{DocsStrings.ABOUT_CURRENT_AUTH_USER}. {DocsStrings.JUST_COMMON_USER_ACCESS}",
)
async def get_me(user_id: CommonUserIDDep, db: DBDep) -> list[Transaction]:
    return await TransactionService(db).get_transactions_by_user_id(user_id)


@router.post(
    "/",
    summary="Обработка платежа",
    description="Получение и обработка данных о платеже от сторонней платежной системы. Например, пополнение счета",
)
async def add_transaction(
    db: DBDep,
    data: TransactionAddRequest = Body(openapi_examples=DocsExamples.TRANSACTION_EXAMPLES),
) -> StatusOK:
    try:
        await TransactionService(db).add_transaction(data)
    except IncorrectTransactionException:
        raise IncorrectTransactionHTTPException
    except TransactionAlreadyExistsException:
        raise NotUniqueTransactionHTTPException
    return StatusOK
