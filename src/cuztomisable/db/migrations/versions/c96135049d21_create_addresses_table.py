"""create_addresses_table

Revision ID: c96135049d21
Revises: 67218e078f1b
Create Date: 2026-06-26 22:03:22.474090

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c96135049d21'
down_revision: Union[str, Sequence[str], None] = '67218e078f1b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('addresses',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('deleted_by', sa.Uuid(), nullable=True),
        sa.Column('created_by', sa.Uuid(), nullable=True),
        sa.Column('user_id', sa.Uuid(), nullable=False),
        sa.Column('address', sa.String(), nullable=True),
        sa.Column('address_two', sa.String(), nullable=True),
        sa.Column('address_three', sa.String(), nullable=True),
        sa.Column('city', sa.String(length=64), nullable=True),
        sa.Column('state_or_province', sa.String(length=64), nullable=True),
        sa.Column('country', sa.String(length=64), nullable=True),
        sa.Column('zip_or_postal_code', sa.String(length=16), nullable=True),
        sa.Column('default', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('shipping', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('billing', sa.Boolean(), nullable=False, server_default='false'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['created_by'], ['users.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['deleted_by'], ['users.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_addresses_user_id', 'addresses', ['user_id'])


def downgrade() -> None:
    op.drop_index('ix_addresses_user_id', table_name='addresses')
    op.drop_table('addresses')
