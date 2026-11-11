"""add last few columns

Revision ID: 5a4cd9d79560
Revises: 51cff23ec3a2
Create Date: 2026-11-10 03:19:48.423586

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5a4cd9d79560'
down_revision: Union[str, Sequence[str], None] = '51cff23ec3a2'  # previous revision ID
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')))
    pass


def downgrade() :
    op.drop_column('posts', 'created_at')
    pass