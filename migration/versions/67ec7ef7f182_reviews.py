"""reviews

Revision ID: 67ec7ef7f182
Revises: a3983a00cdef
Create Date: 2023-07-02 16:30:38.869460

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '67ec7ef7f182'
down_revision = 'a3983a00cdef'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('reviews',
                    sa.Column('id', sa.CHAR(32), nullable=False),
                    sa.Column('text', sa.Text(), nullable=True),
                    sa.Column('branch', sa.String(length=10), nullable=False),
                    sa.Column('author_id', sa.CHAR(32), nullable=False),
                    sa.PrimaryKeyConstraint('id')
                    )


def downgrade() -> None:
    op.drop_table('reviews')
