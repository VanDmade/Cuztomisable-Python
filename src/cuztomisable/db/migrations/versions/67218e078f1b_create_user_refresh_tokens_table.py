"""create_user_refresh_tokens_table

Revision ID: 67218e078f1b
Revises: bc87b311a0f6
Create Date: 2026-06-26 22:03:20.933327

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '67218e078f1b'
down_revision: Union[str, Sequence[str], None] = 'bc87b311a0f6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
