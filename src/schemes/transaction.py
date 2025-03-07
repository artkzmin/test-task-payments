from pydantic import BaseModel


class TransactionBase(BaseModel):
    amount: float


class Transaction(TransactionBase):
    id: str


# Схема для добавления в БД
class TransactionAdd(TransactionBase):
    account_id: int
    id: str


# Схема для получения данных от "сторонней системы"
class TransactionAddRequest(TransactionBase):
    transaction_id: str
    signature: str
    user_id: int
    account_id: int
