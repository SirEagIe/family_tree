"""empty message

Revision ID: 11dcc023a6bd
Revises: af9650e0663d
Create Date: 2021-05-03 22:01:02.120663

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '11dcc023a6bd'
down_revision = 'af9650e0663d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('human', sa.Column('date_of_birthday', sa.Date(), nullable=True))
    op.drop_column('human', 'date_of_bithday')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('human', sa.Column('date_of_bithday', sa.DATE(), nullable=True))
    op.drop_column('human', 'date_of_birthday')
    # ### end Alembic commands ###
