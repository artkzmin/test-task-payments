import typing
from src.database import BaseOrm
from src.schemes.user import UserRoleEnum

from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import Enum


if typing.TYPE_CHECKING:
    from src.models.account import AccountOrm


class UserOrm(BaseOrm):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    name: Mapped[str]
    surname: Mapped[str]
    patronymic: Mapped[str]
    role: Mapped[UserRoleEnum] = mapped_column(Enum(UserRoleEnum), default=UserRoleEnum.COMMON)
    hashed_password: Mapped[str]

    accounts: Mapped[list["AccountOrm"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
