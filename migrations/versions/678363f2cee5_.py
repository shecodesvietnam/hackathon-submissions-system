"""empty message

Revision ID: 678363f2cee5
Revises: d14c27318977
Create Date: 2021-07-24 21:38:51.324846

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '678363f2cee5'
down_revision = 'd14c27318977'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index(op.f('ix_project_name'), 'project', ['name'], unique=True)
    op.add_column('users', sa.Column('has_confirm', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'has_confirm')
    op.drop_index(op.f('ix_project_name'), table_name='project')
    # ### end Alembic commands ###
