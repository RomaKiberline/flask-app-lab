"""Initial migration

Revision ID: ae576d89c8b8
Revises: 
Create Date: 2025-11-26 16:38:26.934864

"""
from alembic import op
import sqlalchemy as sa

revision = 'ae576d89c8b8'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('post',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=150), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('posted', sa.DateTime(), nullable=False),
    sa.Column('category', sa.Enum('news', 'publication', 'tech', 'other', name='categoryenum'), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('author', sa.String(length=20), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('post')
