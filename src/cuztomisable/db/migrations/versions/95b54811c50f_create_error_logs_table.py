"""create_error_logs_table

Revision ID: 95b54811c50f
Revises: 0d4c9c233928
Create Date: 2026-06-26 22:03:25.546864

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '95b54811c50f'
down_revision: Union[str, Sequence[str], None] = '0d4c9c233928'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
