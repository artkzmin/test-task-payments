"""added user.hashed_password

Revision ID: 64ab042de8a5
Revises: 92f44c229c49
Create Date: 2025-03-04 11:05:17.345612

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "64ab042de8a5"
down_revision: Union[str, None] = "92f44c229c49"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("user", sa.Column("hashed_password", sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_column("user", "hashed_password")
