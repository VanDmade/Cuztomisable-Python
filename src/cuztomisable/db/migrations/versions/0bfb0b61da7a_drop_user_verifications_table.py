"""drop_user_verifications_table

Revision ID: 0bfb0b61da7a
Revises: a3f9c1d84e2b
Create Date: 2026-07-16 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '0bfb0b61da7a'
down_revision: Union[str, Sequence[str], None] = 'a3f9c1d84e2b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_index('ix_user_verifications_token', table_name='user_verifications')
    op.drop_index('ix_user_verifications_user_id', table_name='user_verifications')
    op.drop_table('user_verifications')


def downgrade() -> None:
    op.create_table('user_verifications',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('deleted_by', sa.Uuid(), nullable=True),
        sa.Column('user_id', sa.Uuid(), nullable=False),
        sa.Column('type', sa.String(length=5), nullable=False),
        sa.Column('token', sa.String(length=64), nullable=False),
        sa.Column('sent_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('used_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('attempt_counter', sa.Integer(), nullable=False, server_default='0'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['deleted_by'], ['users.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_user_verifications_user_id', 'user_verifications', ['user_id'])
    op.create_index('ix_user_verifications_token', 'user_verifications', ['token'], unique=True)
