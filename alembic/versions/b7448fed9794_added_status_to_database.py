"""Added status to database

Revision ID: b7448fed9794
Revises: 3b95eef01c11
Create Date: 2024-07-10 18:53:22.142140

"""
from typing import Sequence, Union

import sqlalchemy_utils
from alembic import op
import sqlalchemy as sa

from database import models

# revision identifiers, used by Alembic.
revision: str = 'b7448fed9794'
down_revision: Union[str, None] = '3b95eef01c11'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('nodes', sa.Column('status', sqlalchemy_utils.types.choice.ChoiceType(models.Node.STATUS), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('nodes', 'status')
    # ### end Alembic commands ###
