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
    op.create_table('user_ip_addresses',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('deleted_by', sa.Uuid(), nullable=True),
        sa.Column('user_id', sa.Uuid(), nullable=False),
        sa.Column('ip_address', sa.String(length=15), nullable=False),
        sa.Column('label', sa.String(), nullable=True),
        sa.Column('fingerprint', sa.String(length=128), nullable=True),
        sa.Column('last_used_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('remember', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('remember_until', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['deleted_by'], ['users.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_user_ip_addresses_user_id', 'user_ip_addresses', ['user_id'])


def downgrade() -> None:
    op.drop_index('ix_user_ip_addresses_user_id', table_name='user_ip_addresses')
    op.drop_table('user_ip_addresses')
