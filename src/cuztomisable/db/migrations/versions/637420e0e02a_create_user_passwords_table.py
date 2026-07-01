"""create_user_passwords_table

Revision ID: 637420e0e02a
Revises: 7df46c2f0e3d
Create Date: 2026-06-26 22:03:16.295122

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '637420e0e02a'
down_revision: Union[str, Sequence[str], None] = '7df46c2f0e3d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('user_passwords',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('created_by', sa.Uuid(), nullable=True),
        sa.Column('user_id', sa.Uuid(), nullable=False),
        sa.Column('password', sa.String(length=64), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['created_by'], ['users.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_user_passwords_user_id', 'user_passwords', ['user_id'])


def downgrade() -> None:
    op.drop_index('ix_user_passwords_user_id', table_name='user_passwords')
    op.drop_table('user_passwords')
