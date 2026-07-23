"""drop_token_from_user_password_resets

Revision ID: 45525054f855
Revises: 0bfb0b61da7a
Create Date: 2026-07-22 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '45525054f855'
down_revision: Union[str, Sequence[str], None] = '0bfb0b61da7a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column('user_password_resets', 'token')


def downgrade() -> None:
    op.add_column('user_password_resets', sa.Column('token', sa.String(length=64), nullable=True))
