"""expense table

Revision ID: c719d96b6e7c
Revises: af4d825546ee
Create Date: 2024-02-02 09:40:18.467848

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c719d96b6e7c'
down_revision = 'af4d825546ee'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('expense',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(length=255), nullable=False),
    sa.Column('amount', sa.Float(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('expense', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_expense_timestamp'), ['timestamp'], unique=False)
        batch_op.create_index(batch_op.f('ix_expense_user_id'), ['user_id'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('expense', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_expense_user_id'))
        batch_op.drop_index(batch_op.f('ix_expense_timestamp'))

    op.drop_table('expense')
    # ### end Alembic commands ###