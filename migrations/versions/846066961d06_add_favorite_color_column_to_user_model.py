"""Add favorite_color column to User model

Revision ID: 846066961d06
Revises: 
Create Date: 2024-08-01 22:12:25.757172

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '846066961d06'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('favorite_color', sa.String(length=120), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('favorite_color')

    # ### end Alembic commands ###
