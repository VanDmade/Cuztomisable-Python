"""add_image_id_to_users_table

Revision ID: 9c5690dad8ab
Revises: 6606c63083f4
Create Date: 2024-04-12 00:13:26

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '9c5690dad8ab'
down_revision: Union[str, Sequence[str], None] = '6606c63083f4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('image_id', sa.Uuid(), nullable=True))
    op.create_foreign_key(
        'fk_users_image_id', 'users', 'images', ['image_id'], ['id'], ondelete='SET NULL'
    )


def downgrade() -> None:
    op.drop_constraint('fk_users_image_id', 'users', type_='foreignkey')
    op.drop_column('users', 'image_id')
