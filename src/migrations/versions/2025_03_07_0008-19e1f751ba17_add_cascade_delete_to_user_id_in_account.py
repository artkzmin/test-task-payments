"""Add cascade delete to user_id in account

Revision ID: 19e1f751ba17
Revises: fa9abf372b5a
Create Date: 2025-03-07 00:08:27.862496

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa  # noqa: F401


# revision identifiers, used by Alembic.
revision: str = "19e1f751ba17"
down_revision: Union[str, None] = "fa9abf372b5a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint("account_user_id_fkey", "account", type_="foreignkey")
    op.create_foreign_key(None, "account", "user", ["user_id"], ["id"], ondelete="CASCADE")


def downgrade() -> None:
    op.drop_constraint(None, "account", type_="foreignkey")
    op.create_foreign_key("account_user_id_fkey", "account", "user", ["user_id"], ["id"])
