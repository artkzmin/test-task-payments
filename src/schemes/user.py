from pydantic import BaseModel, EmailStr, ConfigDict
from enum import Enum
from src.schemes.account import AccountWithoutUserID


class UserRoleEnum(Enum):
    COMMON = "common"  # Обычный пользователь
    ADMIN = "admin"


class UserBase(BaseModel):
    email: EmailStr
    name: str
    surname: str
    patronymic: str
    role: UserRoleEnum


# Схема для получения данных от слоя представления (API) при регистрации
class UserAddRequest(UserBase):
    password: str


# Схема для добавления в БД
class UserAdd(UserBase):
    hashed_password: str


# Схема для внешнего пользователя (без пароля)
class User(UserBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class UserWithHashedPassword(User):
    hashed_password: str


class UserPatchBase(BaseModel):
    email: EmailStr | None = None
    name: str | None = None
    surname: str | None = None
    patronymic: str | None = None
    role: UserRoleEnum | None = None


# Схема для частичного обновления данных пользователя
class UserPatchRequest(UserPatchBase):
    password: str | None = None


class UserPatch(UserPatchBase):
    hashed_password: str | None = None


class UserAuthRequest(BaseModel):
    email: EmailStr
    password: str


class UserWithReals(User):
    accounts: list[AccountWithoutUserID]


class UserWithFullName(BaseModel):
    id: int
    full_name: str
    email: EmailStr
