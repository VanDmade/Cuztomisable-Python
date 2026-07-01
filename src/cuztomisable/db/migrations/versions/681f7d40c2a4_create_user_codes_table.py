"""create_user_codes_table

Revision ID: 681f7d40c2a4
Revises: 3d158cb3a919
Create Date: 2026-06-26 22:03:17.852891

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '681f7d40c2a4'
down_revision: Union[str, Sequence[str], None] = '3d158cb3a919'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('user_codes',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('deleted_by', sa.Uuid(), nullable=True),
        sa.Column('user_id', sa.Uuid(), nullable=False),
        sa.Column('user_ip_address_id', sa.Uuid(), nullable=True),
        sa.Column('code', sa.String(length=16), nullable=True),
        sa.Column('token', sa.String(length=64), nullable=True),
        sa.Column('used_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('sent_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('sent_via', sa.String(length=5), nullable=True),
        sa.Column('attempt_counter', sa.Integer(), nullable=False, server_default='0'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_ip_address_id'], ['user_ip_addresses.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['deleted_by'], ['users.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_user_codes_user_id', 'user_codes', ['user_id'])


def downgrade() -> None:
    op.drop_index('ix_user_codes_user_id', table_name='user_codes')
    op.drop_table('user_codes')
