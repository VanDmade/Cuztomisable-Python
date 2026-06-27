"""create_roles_table

Revision ID: 380d2030824f
Revises: 9c5690dad8ab
Create Date: 2026-06-26 22:03:13.217663

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '380d2030824f'
down_revision: Union[str, Sequence[str], None] = '9c5690dad8ab'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
