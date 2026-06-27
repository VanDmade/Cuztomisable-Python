"""create_permissions_table

Revision ID: 9534d7f71bb7
Revises: 380d2030824f
Create Date: 2026-06-26 22:03:13.997604

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9534d7f71bb7'
down_revision: Union[str, Sequence[str], None] = '380d2030824f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
