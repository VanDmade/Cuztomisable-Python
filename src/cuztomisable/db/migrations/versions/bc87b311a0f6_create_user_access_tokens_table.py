"""create_user_access_tokens_table

Revision ID: bc87b311a0f6
Revises: b69366609883
Create Date: 2026-06-26 22:03:20.170400

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bc87b311a0f6'
down_revision: Union[str, Sequence[str], None] = 'b69366609883'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
