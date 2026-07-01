"""create_images_table

Revision ID: 6606c63083f4
Revises: 204e726af946
Create Date: 2026-06-26 14:28:54.140777

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6606c63083f4'
down_revision: Union[str, Sequence[str], None] = '204e726af946'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('images',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('deleted_by', sa.Uuid(), nullable=True),
        sa.Column('created_by', sa.Uuid(), nullable=True),
        sa.Column('user_id', sa.Uuid(), nullable=False),
        sa.Column('created_from_image_id', sa.Uuid(), nullable=True),
        sa.Column('name', sa.String(length=64), nullable=False),
        sa.Column('extension', sa.String(length=4), nullable=False),
        sa.Column('path', sa.String(length=1024), nullable=False),
        sa.Column('disk', sa.String(length=64), nullable=False),
        sa.Column('parameters', sa.Text(), nullable=True),
        sa.Column('original', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('removed_from_storage_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['created_from_image_id'], ['images.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['created_by'], ['users.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['deleted_by'], ['users.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_images_user_id', 'images', ['user_id'])


def downgrade() -> None:
    op.drop_index('ix_images_user_id', table_name='images')
    op.drop_table('images')
