"""empty message

Revision ID: ae32bcde1057
Revises: f16a20fe666c
Create Date: 2020-09-10 15:56:10.879289

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ae32bcde1057'
down_revision = 'f16a20fe666c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('games', sa.Column('has_started', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('games', 'has_started')
    # ### end Alembic commands ###
