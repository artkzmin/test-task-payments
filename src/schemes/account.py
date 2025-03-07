from pydantic import BaseModel


class AccountBase(BaseModel):
    id: int
    balance: float


class AccountAdd(AccountBase):
    user_id: int


class Account(AccountBase):
    user_id: int


class AccountPatch(BaseModel):
    balance: int | None = None


class AccountWithoutUserID(AccountBase):
    pass
