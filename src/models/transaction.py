from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship
import typing
from src.database import BaseOrm

if typing.TYPE_CHECKING:
    from src.models.account import AccountOrm


class TransactionOrm(BaseOrm):
    __tablename__ = "transaction"
    id: Mapped[str] = mapped_column(primary_key=True)
    amount: Mapped[float]
    account_id: Mapped[int] = mapped_column(ForeignKey("account.id", ondelete="CASCADE"))

    account: Mapped["AccountOrm"] = relationship(back_populates="transactions")
