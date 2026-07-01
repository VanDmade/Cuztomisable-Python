"""add_role_id_to_users_table

Revision ID: aab10001c0de
Revises: 380d2030824f
Create Date: 2024-04-12 00:15:20

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'aab10001c0de'
down_revision: Union[str, Sequence[str], None] = '380d2030824f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('role_id', sa.Uuid(), nullable=True))
    op.create_foreign_key(
        'fk_users_role_id', 'users', 'roles', ['role_id'], ['id'], ondelete='SET NULL'
    )


def downgrade() -> None:
    op.drop_constraint('fk_users_role_id', 'users', type_='foreignkey')
    op.drop_column('users', 'role_id')
