"""add username to User model

Revision ID: 33251cd99f28
Revises: 5277021a51cf
Create Date: 2020-03-27 15:59:55.450039

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '33251cd99f28'
down_revision = '5277021a51cf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('username', sa.String(), nullable=True))
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_column('user', 'username')
    # ### end Alembic commands ###
