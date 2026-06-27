"""create_user_permissions_table

Revision ID: 80c90b86d5ee
Revises: 681f7d40c2a4
Create Date: 2026-06-26 22:03:18.631830

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '80c90b86d5ee'
down_revision: Union[str, Sequence[str], None] = '681f7d40c2a4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
