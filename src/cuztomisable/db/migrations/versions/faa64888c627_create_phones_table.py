"""create_phones_table

Revision ID: faa64888c627
Revises: 67218e078f1b
Create Date: 2026-06-26 22:03:21.700166

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'faa64888c627'
down_revision: Union[str, Sequence[str], None] = '67218e078f1b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
