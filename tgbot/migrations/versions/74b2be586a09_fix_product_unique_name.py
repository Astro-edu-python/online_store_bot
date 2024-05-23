"""fix_product_unique_name

Revision ID: 74b2be586a09
Revises: 7c6a1a9169e4
Create Date: 2024-05-13 17:05:07.256377

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '74b2be586a09'
down_revision: Union[str, None] = '7c6a1a9169e4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'products', ['name'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'products', type_='unique')
    # ### end Alembic commands ###
