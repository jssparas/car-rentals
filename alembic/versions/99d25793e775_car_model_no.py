"""car model_no

Revision ID: 99d25793e775
Revises: 
Create Date: 2021-11-28 09:02:53.879599

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '99d25793e775'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('car', sa.Column('model_no', sa.String(), nullable=True))
    op.create_unique_constraint('car_model_no_key', 'car', ['model_no'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('car_model_no_key', 'car', type_='unique')
    op.drop_column('car', 'model_no')
    # ### end Alembic commands ###
