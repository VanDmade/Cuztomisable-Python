"""create_user_registrations_table

Revision ID: b69366609883
Revises: 80c90b86d5ee
Create Date: 2026-06-26 22:03:19.384821

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b69366609883'
down_revision: Union[str, Sequence[str], None] = '80c90b86d5ee'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
