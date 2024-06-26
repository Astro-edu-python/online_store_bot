"""users_init

Revision ID: 285f3d3d28d1
Revises: 
Create Date: 2024-04-28 16:24:06.603625

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '285f3d3d28d1'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tg_users',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('phone_number', sa.BigInteger(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tg_users')
    # ### end Alembic commands ###
