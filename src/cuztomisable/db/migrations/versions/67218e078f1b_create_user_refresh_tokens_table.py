"""create_user_refresh_tokens_table

Revision ID: 67218e078f1b
Revises: bc87b311a0f6
Create Date: 2026-06-26 22:03:20.933327

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '67218e078f1b'
down_revision: Union[str, Sequence[str], None] = 'bc87b311a0f6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('user_refresh_tokens',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('user_id', sa.Uuid(), nullable=False),
        sa.Column('token', sa.String(length=64), nullable=False),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('used_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('revoked', sa.Boolean(), nullable=False, server_default='false'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_user_refresh_tokens_user_id', 'user_refresh_tokens', ['user_id'])
    op.create_index('ix_user_refresh_tokens_token', 'user_refresh_tokens', ['token'], unique=True)


def downgrade() -> None:
    op.drop_index('ix_user_refresh_tokens_token', table_name='user_refresh_tokens')
    op.drop_index('ix_user_refresh_tokens_user_id', table_name='user_refresh_tokens')
    op.drop_table('user_refresh_tokens')
