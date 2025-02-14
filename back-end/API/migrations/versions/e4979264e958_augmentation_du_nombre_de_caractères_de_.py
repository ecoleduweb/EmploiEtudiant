"""Augmentation du nombre de caractères de divers champs dans la BD

Revision ID: e4979264e958
Revises: beff9821924a
Create Date: 2024-04-29 09:41:10.450671

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'e4979264e958'
down_revision = 'beff9821924a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('employment_schedule', schema=None) as batch_op:
        batch_op.alter_column('description',
               existing_type=mysql.VARCHAR(length=50),
               type_=sa.String(length=100),
               existing_nullable=False)

    with op.batch_alter_table('job_offer', schema=None) as batch_op:
        batch_op.alter_column('description',
               existing_type=sa.String(length=255),
               type_=mysql.MEDIUMTEXT(),
               existing_nullable=False)
        
        batch_op.alter_column('approbationMessage',
               existing_type=sa.String(length=255),
               type_=mysql.VARCHAR(length=6000),
               existing_nullable=True)

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('password',
               existing_type=mysql.VARCHAR(length=255),
               type_=sa.String(length=300),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('password',
               existing_type=sa.String(length=300),
               type_=mysql.VARCHAR(length=255),
               existing_nullable=True)

    with op.batch_alter_table('job_offer', schema=None) as batch_op:
        batch_op.alter_column('approbationMessage',
               existing_type=sa.String(length=6000),
               type_=mysql.VARCHAR(length=255),
               existing_nullable=True)
        batch_op.alter_column('description',
               existing_type=mysql.MEDIUMTEXT(),
               type_=sa.String(length=255),
               existing_nullable=False)

    with op.batch_alter_table('employment_schedule', schema=None) as batch_op:
        batch_op.alter_column('description',
               existing_type=mysql.VARCHAR(length=100),
               type_=sa.String(length=50),
               existing_nullable=False)

    # ### end Alembic commands ###
