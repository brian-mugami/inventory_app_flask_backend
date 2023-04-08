"""empty message

Revision ID: 0fa1968f0252
Revises: ed0865cd4b4a
Create Date: 2023-04-08 22:44:05.576261

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0fa1968f0252'
down_revision = 'ed0865cd4b4a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('accounts', schema=None) as batch_op:
        batch_op.alter_column('account_number',
               existing_type=sa.INTEGER(),
               type_=sa.String(length=100),
               existing_nullable=False)
        batch_op.drop_constraint('accounts_account_number_key', type_='unique')
        batch_op.create_unique_constraint('account_unique_check', ['account_name', 'account_number', 'account_category'])

    with op.batch_alter_table('items', schema=None) as batch_op:
        batch_op.alter_column('price',
               existing_type=sa.REAL(),
               type_=sa.Float(precision=2),
               existing_nullable=False)

    with op.batch_alter_table('purchases', schema=None) as batch_op:
        batch_op.alter_column('buying_price',
               existing_type=sa.REAL(),
               type_=sa.Float(precision=4),
               existing_nullable=False)
        batch_op.alter_column('item_cost',
               existing_type=sa.REAL(),
               type_=sa.Float(precision=2),
               existing_nullable=False)
        batch_op.alter_column('lines_cost',
               existing_type=sa.REAL(),
               type_=sa.Float(precision=2),
               existing_nullable=False)

    with op.batch_alter_table('receipts', schema=None) as batch_op:
        batch_op.alter_column('amount',
               existing_type=sa.REAL(),
               type_=sa.Float(precision=4),
               existing_nullable=True)

    with op.batch_alter_table('sales', schema=None) as batch_op:
        batch_op.alter_column('selling_price',
               existing_type=sa.REAL(),
               type_=sa.Float(precision=4),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('sales', schema=None) as batch_op:
        batch_op.alter_column('selling_price',
               existing_type=sa.Float(precision=4),
               type_=sa.REAL(),
               existing_nullable=False)

    with op.batch_alter_table('receipts', schema=None) as batch_op:
        batch_op.alter_column('amount',
               existing_type=sa.Float(precision=4),
               type_=sa.REAL(),
               existing_nullable=True)

    with op.batch_alter_table('purchases', schema=None) as batch_op:
        batch_op.alter_column('lines_cost',
               existing_type=sa.Float(precision=2),
               type_=sa.REAL(),
               existing_nullable=False)
        batch_op.alter_column('item_cost',
               existing_type=sa.Float(precision=2),
               type_=sa.REAL(),
               existing_nullable=False)
        batch_op.alter_column('buying_price',
               existing_type=sa.Float(precision=4),
               type_=sa.REAL(),
               existing_nullable=False)

    with op.batch_alter_table('items', schema=None) as batch_op:
        batch_op.alter_column('price',
               existing_type=sa.Float(precision=2),
               type_=sa.REAL(),
               existing_nullable=False)

    with op.batch_alter_table('accounts', schema=None) as batch_op:
        batch_op.drop_constraint('account_unique_check', type_='unique')
        batch_op.create_unique_constraint('accounts_account_number_key', ['account_number'])
        batch_op.alter_column('account_number',
               existing_type=sa.String(length=100),
               type_=sa.INTEGER(),
               existing_nullable=False)

    # ### end Alembic commands ###
