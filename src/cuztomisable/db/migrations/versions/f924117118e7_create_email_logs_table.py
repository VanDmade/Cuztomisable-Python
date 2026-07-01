"""create_email_logs_table

Revision ID: f924117118e7
Revises: 67d85c934772
Create Date: 2026-06-26 22:03:24.000477

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f924117118e7'
down_revision: Union[str, Sequence[str], None] = '67d85c934772'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('email_logs',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('created_by', sa.Uuid(), nullable=True),
        sa.Column('to', sa.Text(), nullable=True),
        sa.Column('cc', sa.Text(), nullable=True),
        sa.Column('bcc', sa.Text(), nullable=True),
        sa.Column('from', sa.String(length=128), nullable=True),
        sa.Column('subject', sa.String(length=512), nullable=True),
        sa.Column('parameters', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['created_by'], ['users.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id'),
    )


def downgrade() -> None:
    op.drop_table('email_logs')
