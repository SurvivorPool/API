"""empty message

Revision ID: 0c4fb0c4b4d4
Revises: 3bbf2c32609a
Create Date: 2020-11-28 03:16:07.924065

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0c4fb0c4b4d4'
down_revision = '3bbf2c32609a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('games', 'day_of_week',
               existing_type=sa.VARCHAR(length=8),
               type_=sa.String(length=12),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('games', 'day_of_week',
               existing_type=sa.String(length=12),
               type_=sa.VARCHAR(length=8),
               existing_nullable=True)
    # ### end Alembic commands ###
