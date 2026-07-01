"""create_users_table

Revision ID: 204e726af946
Revises: 
Create Date: 2026-06-26 14:28:34.527527

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '204e726af946'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('deleted_by', sa.Uuid(), nullable=True),
        sa.Column('created_by', sa.Uuid(), nullable=True),
        sa.Column('name', sa.String(length=128), nullable=False),
        sa.Column('username', sa.String(length=128), nullable=True),
        sa.Column('email', sa.String(length=128), nullable=False),
        sa.Column('email_verified_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('disable_emails', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('password', sa.String(length=64), nullable=False),
        sa.Column('timezone', sa.String(length=64), nullable=True),
        sa.Column('locked', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('change_password', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('change_password_sent_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('multi_factor_authentication', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('admin', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('attempts', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('attempt_timer', sa.DateTime(timezone=True), nullable=True),
        sa.Column('token', sa.String(length=32), nullable=True),
        sa.ForeignKeyConstraint(['created_by'], ['users.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['deleted_by'], ['users.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_users_email', 'users', ['email'], unique=True)
    op.create_index('ix_users_username', 'users', ['username'], unique=True)
    op.create_index('ix_users_token', 'users', ['token'], unique=True)


def downgrade() -> None:
    op.drop_index('ix_users_token', table_name='users')
    op.drop_index('ix_users_username', table_name='users')
    op.drop_index('ix_users_email', table_name='users')
    op.drop_table('users')
