"""empty message

Revision ID: 366e701bd64f
Revises: 
Create Date: 2021-07-27 00:02:32.721438

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


# revision identifiers, used by Alembic.
revision = '366e701bd64f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('role',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('has_confirm', sa.Boolean(), nullable=True),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['role.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    op.create_table('project',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('team_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('slide', sqlalchemy_utils.types.url.URLType(), nullable=True),
    sa.Column('github', sqlalchemy_utils.types.url.URLType(), nullable=True),
    sa.Column('youtube', sqlalchemy_utils.types.url.URLType(), nullable=True),
    sa.Column('timestamp', sa.String(length=100), nullable=True),
    sa.ForeignKeyConstraint(['team_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_project_name'), 'project', ['name'], unique=True)
    op.create_index(op.f('ix_project_timestamp'), 'project', ['timestamp'], unique=False)
    op.create_table('graderound1',
    sa.Column('mentor_id', sa.Integer(), nullable=False),
    sa.Column('project_id', sa.Integer(), nullable=False),
    sa.Column('total', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['mentor_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['project_id'], ['project.id'], ),
    sa.PrimaryKeyConstraint('mentor_id', 'project_id')
    )
    op.create_table('graderound2',
    sa.Column('judge_id', sa.Integer(), nullable=False),
    sa.Column('project_id', sa.Integer(), nullable=False),
    sa.Column('total', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['judge_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['project_id'], ['project.id'], ),
    sa.PrimaryKeyConstraint('judge_id', 'project_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('graderound2')
    op.drop_table('graderound1')
    op.drop_index(op.f('ix_project_timestamp'), table_name='project')
    op.drop_index(op.f('ix_project_name'), table_name='project')
    op.drop_table('project')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    op.drop_table('role')
    # ### end Alembic commands ###