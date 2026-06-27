"""create_text_logs_table

Revision ID: 0d4c9c233928
Revises: f924117118e7
Create Date: 2026-06-26 22:03:24.772294

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0d4c9c233928'
down_revision: Union[str, Sequence[str], None] = 'f924117118e7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
