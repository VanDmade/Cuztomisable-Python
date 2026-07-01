"""create_text_logs_table

Revision ID: 0d4c9c233928
Revises: f924117118e7
Create Date: 2026-06-26 22:03:24.772294

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0d4c9c233928'
down_revision: Union[str, Sequence[str], None] = 'f924117118e7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('text_logs',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('created_by', sa.Uuid(), nullable=True),
        sa.Column('number', sa.String(length=13), nullable=True),
        sa.Column('country_code', sa.String(length=3), nullable=True),
        sa.Column('message', sa.Text(), nullable=True),
        sa.Column('parameters', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['created_by'], ['users.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id'),
    )


def downgrade() -> None:
    op.drop_table('text_logs')
