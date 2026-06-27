"""create_user_ip_addresses_table

Revision ID: 7df46c2f0e3d
Revises: 1286c32eaad1
Create Date: 2026-06-26 22:03:15.523622

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7df46c2f0e3d'
down_revision: Union[str, Sequence[str], None] = '1286c32eaad1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
