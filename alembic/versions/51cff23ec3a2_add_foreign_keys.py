""" add foreign keys

Revision ID: 51cff23ec3a2
Revises: 15807d6b21d1
Create Date: 2026-11-10 03:18:27.967674

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '51cff23ec3a2'
down_revision: Union[str, Sequence[str], None] = '15807d6b21d1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade() :
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table='posts', referent_table='users', local_cols=['owner_id'], remote_cols=['id'], ondelete='CASCADE')
    pass


def downgrade() :
    op.drop_constraint('post_users_fk', table_name='posts')
    op.drop_column('posts', 'owner_id')