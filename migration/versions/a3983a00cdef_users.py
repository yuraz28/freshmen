"""users

Revision ID: a3983a00cdef
Revises: 
Create Date: 2023-07-02 13:23:07.587100

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'a3983a00cdef'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column('id', sa.CHAR(32), nullable=False),
                    sa.Column('name', sa.String(length=100), nullable=False),
                    sa.Column('email', sa.String(length=100), nullable=False),
                    sa.Column('password_hash', sa.String(length=128), nullable=False),
                    sa.Column('is_user', sa.BOOLEAN, nullable=False),
                    sa.Column('place_study', sa.String(length=100), nullable=False),
                    sa.Column('branch', sa.String(length=10), nullable=False),
                    sa.Column('course', sa.SmallInteger(), nullable=False),
                    sa.PrimaryKeyConstraint('id')
                    )


def downgrade() -> None:
    op.drop_table('users')
