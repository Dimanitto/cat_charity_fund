"""empty migration for pytest

Revision ID: 0002
Revises: 0001
Create Date: 2023-04-13 15:42:20.006028
"""
# Без этой миграции не проходил pytest. Почему-то первую миграцию не видели тесты
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0002'
down_revision = '0001'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###