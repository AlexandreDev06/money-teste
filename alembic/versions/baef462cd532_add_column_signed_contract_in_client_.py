"""add column signed_contract in client table

Revision ID: baef462cd532
Revises: 82b84d4aafa5
Create Date: 2023-09-28 17:13:55.403240

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'baef462cd532'
down_revision: Union[str, None] = '82b84d4aafa5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('client_operations', 'is_signed')
    op.add_column('clients', sa.Column('signed_contract', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('clients', 'signed_contract')
    op.add_column('client_operations', sa.Column('is_signed', sa.BOOLEAN(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
