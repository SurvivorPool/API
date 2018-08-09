"""empty message

Revision ID: 8ebef6ea74ae
Revises: de8f05fc7f7b
Create Date: 2018-08-06 22:34:10.264921

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8ebef6ea74ae'
down_revision = 'de8f05fc7f7b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('picks',
    sa.Column('pick_id', sa.Integer(), nullable=False),
    sa.Column('team_id', sa.Integer(), nullable=False),
    sa.Column('game_id', sa.Integer(), nullable=False),
    sa.Column('week_num', sa.Integer(), nullable=False),
    sa.Column('nfl_team_name', sa.String(length=30), nullable=False),
    sa.ForeignKeyConstraint(['game_id'], ['games.game_id'], ),
    sa.ForeignKeyConstraint(['team_id'], ['player_teams.team_id'], ),
    sa.PrimaryKeyConstraint('pick_id')
    )
    op.drop_table('pick_model')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('pick_model',
    sa.Column('pick_id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('team_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('game_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('week_num', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('nfl_team_name', sa.VARCHAR(length=30), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['game_id'], ['games.game_id'], name='pick_model_game_id_fkey'),
    sa.ForeignKeyConstraint(['team_id'], ['player_teams.team_id'], name='pick_model_team_id_fkey'),
    sa.PrimaryKeyConstraint('pick_id', name='pick_model_pkey')
    )
    op.drop_table('picks')
    # ### end Alembic commands ###