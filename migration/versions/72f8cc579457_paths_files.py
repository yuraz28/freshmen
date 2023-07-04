"""paths_files

Revision ID: 72f8cc579457
Revises: 67ec7ef7f182
Create Date: 2023-07-04 10:39:12.536042

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '72f8cc579457'
down_revision = '67ec7ef7f182'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('paths_files',
                    sa.Column('id', sa.CHAR(32), nullable=False),
                    sa.Column('name', sa.String(length=100), nullable=False),
                    sa.Column('place_study', sa.String(length=100), nullable=False),
                    sa.Column('branch', sa.String(length=10), nullable=False),
                    sa.Column('author_id', sa.CHAR(32), nullable=False),
                    sa.Column('is_private', sa.BOOLEAN, nullable=False),
                    sa.Column('course', sa.SmallInteger(), nullable=False),
                    sa.PrimaryKeyConstraint('id')
                    )


def downgrade() -> None:
    op.drop_table('paths_files')
