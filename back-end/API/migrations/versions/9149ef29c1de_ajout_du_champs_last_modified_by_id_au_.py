"""Ajout du champs last_modified_by_id au job_offer

Revision ID: 9149ef29c1de
Revises: cace79e373d8
Create Date: 2024-08-31 16:07:47.588879

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '9149ef29c1de'
down_revision = 'cace79e373d8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('job_offer', schema=None) as batch_op:
        batch_op.add_column(sa.Column('last_modified_by_id', sa.Integer(), nullable=True))
        batch_op.alter_column('description',
               existing_type=mysql.MEDIUMTEXT(),
               type_=sa.Text(length=30000),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('job_offer', schema=None) as batch_op:
        batch_op.alter_column('description',
               existing_type=sa.Text(length=30000),
               type_=mysql.MEDIUMTEXT(),
               existing_nullable=False)
        batch_op.drop_column('last_modified_by_id')

    # ### end Alembic commands ###
