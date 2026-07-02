"""create_error_logs_table

Revision ID: 95b54811c50f
Revises: 0d4c9c233928
Create Date: 2026-06-26 22:03:25.546864

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '95b54811c50f'
down_revision: Union[str, Sequence[str], None] = '0d4c9c233928'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('error_logs',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('user_id', sa.Uuid(), nullable=True),
        sa.Column('message', sa.Text(), nullable=True),
        sa.Column('line', sa.Integer(), nullable=True),
        sa.Column('file', sa.String(length=256), nullable=True),
        sa.Column('code', sa.String(length=8), nullable=True),
        sa.Column('debug_code', sa.String(length=8), nullable=True),
        sa.Column('parameters', postgresql.JSONB(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id'),
    )


def downgrade() -> None:
    op.drop_table('error_logs')
