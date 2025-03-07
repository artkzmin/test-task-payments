import typing
from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship
from src.database import BaseOrm


if typing.TYPE_CHECKING:
    from src.models.transaction import TransactionOrm
    from src.models.user import UserOrm


class AccountOrm(BaseOrm):
    __tablename__ = "account"
    id: Mapped[int] = mapped_column(primary_key=True)
    balance: Mapped[float]
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))

    user: Mapped["UserOrm"] = relationship(back_populates="accounts")
    transactions: Mapped[list["TransactionOrm"]] = relationship(
        back_populates="account", cascade="all, delete-orphan"
    )
