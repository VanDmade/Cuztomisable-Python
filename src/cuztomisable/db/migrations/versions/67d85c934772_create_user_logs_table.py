"""create_user_logs_table

Revision ID: 67d85c934772
Revises: c96135049d21
Create Date: 2026-06-26 22:03:23.233716

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '67d85c934772'
down_revision: Union[str, Sequence[str], None] = 'c96135049d21'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
