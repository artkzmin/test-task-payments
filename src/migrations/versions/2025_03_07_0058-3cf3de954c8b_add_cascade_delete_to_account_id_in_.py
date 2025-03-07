"""Add cascade delete to account_id in transaction

Revision ID: 3cf3de954c8b
Revises: 19e1f751ba17
Create Date: 2025-03-07 00:58:01.624319

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa  # noqa: F401


# revision identifiers, used by Alembic.
revision: str = "3cf3de954c8b"
down_revision: Union[str, None] = "19e1f751ba17"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint("transaction_account_id_fkey", "transaction", type_="foreignkey")
    op.create_foreign_key(
        None,
        "transaction",
        "account",
        ["account_id"],
        ["id"],
        ondelete="CASCADE",
    )


def downgrade() -> None:
    op.drop_constraint(None, "transaction", type_="foreignkey")
    op.create_foreign_key(
        "transaction_account_id_fkey",
        "transaction",
        "account",
        ["account_id"],
        ["id"],
    )
