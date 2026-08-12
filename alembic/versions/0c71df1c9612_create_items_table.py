"""create items table

Revision ID: 0c71df1c9612
Revises: 
Create Date: 2026-08-12 16:03:23.211761

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0c71df1c9612'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'items',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('price', sa.Float(), nullable=False),
        sa.Column('stock_quantity', sa.Integer(), nullable=False, default=0),
        sa.Column('description', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    op.drop_table('items')
