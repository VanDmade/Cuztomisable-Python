"""create_user_logs_table

Revision ID: 67d85c934772
Revises: c96135049d21
Create Date: 2026-06-26 22:03:23.233716

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '67d85c934772'
down_revision: Union[str, Sequence[str], None] = 'c96135049d21'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('user_logs',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('created_by', sa.Uuid(), nullable=True),
        sa.Column('user_id', sa.Uuid(), nullable=False),
        sa.Column('description', sa.String(length=256), nullable=True),
        sa.Column('parameters', postgresql.JSONB(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['created_by'], ['users.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_user_logs_user_id', 'user_logs', ['user_id'])


def downgrade() -> None:
    op.drop_index('ix_user_logs_user_id', table_name='user_logs')
    op.drop_table('user_logs')
