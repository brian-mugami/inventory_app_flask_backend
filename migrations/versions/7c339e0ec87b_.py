"""empty message

Revision ID: 7c339e0ec87b
Revises: 0737532defe1
Create Date: 2023-01-19 15:30:31.290659

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7c339e0ec87b'
down_revision = '0737532defe1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('items', schema=None) as batch_op:
        batch_op.alter_column('price',
               existing_type=sa.REAL(),
               type_=sa.Float(precision=2),
               existing_nullable=False)
        batch_op.alter_column('category_id',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.drop_constraint('items_category_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key(None, 'categories', ['category_id'], ['id'], ondelete='SET NULL')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('items', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('items_category_id_fkey', 'categories', ['category_id'], ['id'])
        batch_op.alter_column('category_id',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.alter_column('price',
               existing_type=sa.Float(precision=2),
               type_=sa.REAL(),
               existing_nullable=False)

    # ### end Alembic commands ###
