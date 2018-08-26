"""empty message

Revision ID: fcf6dea37283
Revises: 8fb3a0bd4a39
Create Date: 2018-08-25 20:29:02.407438

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fcf6dea37283'
down_revision = '8fb3a0bd4a39'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('games', 'time')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('games', sa.Column('time', sa.VARCHAR(length=10), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
