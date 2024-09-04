"""Models fix 4 - Add expire time for token

Revision ID: 190040b74282
Revises: 4cb410d0de80
Create Date: 2024-09-01 19:59:46.638085

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '190040b74282'
down_revision: Union[str, None] = '4cb410d0de80'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('token', sa.Column('expire_time', sa.DateTime(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('token', 'expire_time')
    # ### end Alembic commands ###
