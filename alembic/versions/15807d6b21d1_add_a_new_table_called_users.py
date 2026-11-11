"""add a new table called users

Revision ID: 15807d6b21d1
Revises: 3c39b63c902d
Create Date: 2026-11-10 03:16:46.042574

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '15807d6b21d1'
down_revision: Union[str, Sequence[str], None] = '3c39b63c902d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('email', sa.String(), nullable=False, unique=True),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone = True), nullable=False, server_default=sa.text('now()')),
                    )
    pass


def downgrade():
    op.drop_table('users')
    pass
