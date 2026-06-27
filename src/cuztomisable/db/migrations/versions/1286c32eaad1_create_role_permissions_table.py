"""create_role_permissions_table

Revision ID: 1286c32eaad1
Revises: 9534d7f71bb7
Create Date: 2026-06-26 22:03:14.772805

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1286c32eaad1'
down_revision: Union[str, Sequence[str], None] = '9534d7f71bb7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
