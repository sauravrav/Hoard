"""Rename password to encrypted_password

Revision ID: 657f5352e4a5
Revises: 3e3a1ce166b1
Create Date: 2024-12-01 17:08:16.348715

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '657f5352e4a5'
down_revision: Union[str, None] = '3e3a1ce166b1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('encrypted_password', sa.String(), nullable=True))
    op.drop_column('users', 'password')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('password', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_column('users', 'encrypted_password')
    # ### end Alembic commands ###
