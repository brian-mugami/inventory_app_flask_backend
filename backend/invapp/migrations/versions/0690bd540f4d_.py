"""empty message

Revision ID: 0690bd540f4d
Revises: 90713a4d7c2e
Create Date: 2023-03-20 00:15:07.141264

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0690bd540f4d'
down_revision = '90713a4d7c2e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###

    with op.batch_alter_table('items', schema=None) as batch_op:
        batch_op.alter_column('price',
               existing_type=sa.REAL(),
               type_=sa.Float(precision=2),
               existing_nullable=False)

    with op.batch_alter_table('purchases', schema=None) as batch_op:
        batch_op.add_column(sa.Column('invoice_number', sa.String(length=256), nullable=False))
        batch_op.add_column(sa.Column('description', sa.String(length=256), nullable=True))
        batch_op.add_column(sa.Column('buying_price', sa.Float(precision=4), nullable=False))
        batch_op.add_column(sa.Column('date_of_supply', sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column('item_id', sa.Integer(), nullable=False))
        batch_op.create_index(batch_op.f('ix_purchases_invoice_number'), ['invoice_number'], unique=True)
        batch_op.create_foreign_key(None, 'items', ['item_id'], ['id'])
        batch_op.drop_column('date_bought')
        batch_op.drop_column('price')

    with op.batch_alter_table('sales', schema=None) as batch_op:
        batch_op.add_column(sa.Column('receipt_number', sa.String(length=256), nullable=False))
        batch_op.add_column(sa.Column('description', sa.String(length=256), nullable=True))
        batch_op.add_column(sa.Column('selling_price', sa.Float(precision=4), nullable=False))
        batch_op.add_column(sa.Column('item_id', sa.Integer(), nullable=False))
        batch_op.create_index(batch_op.f('ix_sales_receipt_number'), ['receipt_number'], unique=True)
        batch_op.create_foreign_key(None, 'items', ['item_id'], ['id'])
        batch_op.drop_column('cost')

    with op.batch_alter_table('suppliers', schema=None) as batch_op:
        batch_op.drop_constraint('suppliers_account_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key(None, 'supplier_account', ['account_id'], ['id'], ondelete='SET DEFAULT')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('suppliers', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('suppliers_account_id_fkey', 'supplier_account', ['account_id'], ['id'])

    with op.batch_alter_table('sales', schema=None) as batch_op:
        batch_op.add_column(sa.Column('cost', sa.REAL(), autoincrement=False, nullable=False))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_index(batch_op.f('ix_sales_receipt_number'))
        batch_op.drop_column('item_id')
        batch_op.drop_column('selling_price')
        batch_op.drop_column('description')
        batch_op.drop_column('receipt_number')

    with op.batch_alter_table('purchases', schema=None) as batch_op:
        batch_op.add_column(sa.Column('price', sa.REAL(), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('date_bought', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_index(batch_op.f('ix_purchases_invoice_number'))
        batch_op.drop_column('item_id')
        batch_op.drop_column('date_of_supply')
        batch_op.drop_column('buying_price')
        batch_op.drop_column('description')
        batch_op.drop_column('invoice_number')

    with op.batch_alter_table('items', schema=None) as batch_op:
        batch_op.alter_column('price',
               existing_type=sa.Float(precision=2),
               type_=sa.REAL(),
               existing_nullable=False)

    with op.batch_alter_table('categories', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('categories_account_id_fkey', 'item_account', ['account_id'], ['id'])

    op.create_table('item_account',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('account_name', sa.VARCHAR(length=80), autoincrement=False, nullable=False),
    sa.Column('account_description', sa.VARCHAR(length=256), autoincrement=False, nullable=True),
    sa.Column('account_number', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('is_active', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('date_created', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('date_archived', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('is_archived', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('date_unarchived', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='item_account_pkey'),
    sa.UniqueConstraint('account_name', name='item_account_account_name_key'),
    sa.UniqueConstraint('account_number', name='item_account_account_number_key')
    )
    # ### end Alembic commands ###
