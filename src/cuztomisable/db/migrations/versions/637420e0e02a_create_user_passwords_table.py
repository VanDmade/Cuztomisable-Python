"""create_user_passwords_table

Revision ID: 637420e0e02a
Revises: 7df46c2f0e3d
Create Date: 2026-06-26 22:03:16.295122

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '637420e0e02a'
down_revision: Union[str, Sequence[str], None] = '7df46c2f0e3d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
