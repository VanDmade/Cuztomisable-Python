"""create_email_logs_table

Revision ID: f924117118e7
Revises: 67d85c934772
Create Date: 2026-06-26 22:03:24.000477

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f924117118e7'
down_revision: Union[str, Sequence[str], None] = '67d85c934772'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
