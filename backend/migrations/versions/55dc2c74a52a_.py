"""empty message

Revision ID: 55dc2c74a52a
Revises: d964377e9f4c
Create Date: 2023-04-03 21:23:41.097907

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '55dc2c74a52a'
down_revision = 'd964377e9f4c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('customer payment accounting', schema=None) as batch_op:
        batch_op.drop_constraint('customer payment accounting_payment_id_balance_id_key', type_='unique')

    with op.batch_alter_table('items', schema=None) as batch_op:
        batch_op.alter_column('price',
               existing_type=sa.REAL(),
               type_=sa.Float(precision=2),
               existing_nullable=False)

    with op.batch_alter_table('purchase accounting', schema=None) as batch_op:
        batch_op.drop_constraint('purchase accounting_invoice_id_key', type_='unique')

    with op.batch_alter_table('purchases', schema=None) as batch_op:
        batch_op.alter_column('buying_price',
               existing_type=sa.REAL(),
               type_=sa.Float(precision=4),
               existing_nullable=False)

    with op.batch_alter_table('sales', schema=None) as batch_op:
        batch_op.alter_column('selling_price',
               existing_type=sa.REAL(),
               type_=sa.Float(precision=4),
               existing_nullable=False)

    with op.batch_alter_table('supplier payment accounting', schema=None) as batch_op:
        batch_op.drop_constraint('supplier payment accounting_payment_id_balance_id_key', type_='unique')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('supplier payment accounting', schema=None) as batch_op:
        batch_op.create_unique_constraint('supplier payment accounting_payment_id_balance_id_key', ['payment_id', 'balance_id'])

    with op.batch_alter_table('sales', schema=None) as batch_op:
        batch_op.alter_column('selling_price',
               existing_type=sa.Float(precision=4),
               type_=sa.REAL(),
               existing_nullable=False)

    with op.batch_alter_table('purchases', schema=None) as batch_op:
        batch_op.alter_column('buying_price',
               existing_type=sa.Float(precision=4),
               type_=sa.REAL(),
               existing_nullable=False)

    with op.batch_alter_table('purchase accounting', schema=None) as batch_op:
        batch_op.create_unique_constraint('purchase accounting_invoice_id_key', ['invoice_id'])

    with op.batch_alter_table('items', schema=None) as batch_op:
        batch_op.alter_column('price',
               existing_type=sa.Float(precision=2),
               type_=sa.REAL(),
               existing_nullable=False)

    with op.batch_alter_table('customer payment accounting', schema=None) as batch_op:
        batch_op.create_unique_constraint('customer payment accounting_payment_id_balance_id_key', ['payment_id', 'balance_id'])

    # ### end Alembic commands ###