"""empty message

Revision ID: 9d882d87efbd
Revises: 8b70d921e6b9
Create Date: 2018-08-24 23:36:07.220313

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9d882d87efbd'
down_revision = '8b70d921e6b9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('games', sa.Column('site_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'games', 'stadiums', ['site_id'], ['stadium_id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'games', type_='foreignkey')
    op.drop_column('games', 'site_id')
    # ### end Alembic commands ###
