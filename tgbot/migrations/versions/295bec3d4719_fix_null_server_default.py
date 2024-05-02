"""fix null server default

Revision ID: 295bec3d4719
Revises: 928fbbf33b11
Create Date: 2024-04-28 17:23:18.799118

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '295bec3d4719'
down_revision: Union[str, None] = '928fbbf33b11'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('tg_users', 'is_admin',
               existing_type=sa.BOOLEAN(),
               server_default='f',
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('tg_users', 'is_admin',
               existing_type=sa.BOOLEAN(),
               server_default=None,
               nullable=True)
    # ### end Alembic commands ###
