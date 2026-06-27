"""create_addresses_table

Revision ID: c96135049d21
Revises: faa64888c627
Create Date: 2026-06-26 22:03:22.474090

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c96135049d21'
down_revision: Union[str, Sequence[str], None] = 'faa64888c627'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
