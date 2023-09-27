"""empty message

Revision ID: 39d3034c8132
Revises: 9b7f05391f6e
Create Date: 2023-06-04 10:31:06.109969

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '39d3034c8132'
down_revision = '9b7f05391f6e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('review', schema=None) as batch_op:
        batch_op.add_column(sa.Column('last_edited', sa.DateTime(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('review', schema=None) as batch_op:
        batch_op.drop_column('last_edited')

    # ### end Alembic commands ###
