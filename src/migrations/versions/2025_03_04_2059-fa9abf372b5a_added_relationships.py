"""added relationships

Revision ID: fa9abf372b5a
Revises: 64ab042de8a5
Create Date: 2025-03-04 20:59:28.595408

"""

from typing import Sequence, Union

from alembic import op  # noqa: F401
import sqlalchemy as sa  # noqa: F401


# revision identifiers, used by Alembic.
revision: str = "fa9abf372b5a"
down_revision: Union[str, None] = "64ab042de8a5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
