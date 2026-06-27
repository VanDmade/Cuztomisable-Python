"""create_user_codes_table

Revision ID: 681f7d40c2a4
Revises: 3d158cb3a919
Create Date: 2026-06-26 22:03:17.852891

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '681f7d40c2a4'
down_revision: Union[str, Sequence[str], None] = '3d158cb3a919'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
