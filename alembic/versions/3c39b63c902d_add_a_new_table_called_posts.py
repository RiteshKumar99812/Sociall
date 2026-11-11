"""add a new table called posts

Revision ID: 3c39b63c902d
Revises: 
Create Date: 2026-11-10 03:15:25.834707

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3c39b63c902d'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table('posts',
                    sa.Column('id', sa.Integer(), nullable=False , primary_key=True),
                    sa.Column('title', sa.String(length=100), nullable=False),
                    sa.Column('content', sa.Text(), nullable=False),
                    sa.Column('published', sa.Boolean(), server_default='TRUE', nullable=False),
                    )


def downgrade() :
    op.drop_table('posts')
    pass
