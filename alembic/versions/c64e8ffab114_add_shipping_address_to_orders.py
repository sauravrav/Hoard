"""Add shipping_address to orders

Revision ID: c64e8ffab114
Revises: 847b793e4cce
Create Date: 2024-11-18 01:31:29.685804

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c64e8ffab114'
down_revision: Union[str, None] = '847b793e4cce'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('orders', sa.Column('shipping_address', sa.String(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('orders', 'shipping_address')
    # ### end Alembic commands ###
