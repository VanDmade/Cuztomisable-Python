"""create_phones_table

Revision ID: faa64888c627
Revises: 67218e078f1b
Create Date: 2026-06-26 22:03:21.700166

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'faa64888c627'
down_revision: Union[str, Sequence[str], None] = '67218e078f1b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('phones',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('deleted_by', sa.Uuid(), nullable=True),
        sa.Column('created_by', sa.Uuid(), nullable=True),
        sa.Column('user_id', sa.Uuid(), nullable=False),
        sa.Column('number', sa.String(length=13), nullable=False),
        sa.Column('country_code', sa.String(length=3), nullable=True),
        sa.Column('extension', sa.String(length=8), nullable=True),
        sa.Column('mobile', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('default', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('verified_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('disable_messages', sa.Boolean(), nullable=False, server_default='false'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['created_by'], ['users.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['deleted_by'], ['users.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_phones_user_id', 'phones', ['user_id'])


def downgrade() -> None:
    op.drop_index('ix_phones_user_id', table_name='phones')
    op.drop_table('phones')
