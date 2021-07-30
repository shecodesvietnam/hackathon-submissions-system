"""empty message

Revision ID: 4a7b16d75c77
Revises: 366e701bd64f
Create Date: 2021-07-30 22:22:34.029994

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


# revision identifiers, used by Alembic.
revision = '4a7b16d75c77'
down_revision = '366e701bd64f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('project', sa.Column('others', sqlalchemy_utils.types.url.URLType(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('project', 'others')
    # ### end Alembic commands ###
