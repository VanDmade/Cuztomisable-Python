"""create_user_password_resets_table

Revision ID: 3d158cb3a919
Revises: 637420e0e02a
Create Date: 2026-06-26 22:03:17.097208

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3d158cb3a919'
down_revision: Union[str, Sequence[str], None] = '637420e0e02a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
