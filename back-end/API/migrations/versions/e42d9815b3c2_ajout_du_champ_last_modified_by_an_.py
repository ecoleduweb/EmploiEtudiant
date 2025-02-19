"""ajout_champ_last_modified_by_an_employer_date_job_offer
Revision ID: e979f6069600
Revises: 0dbb25a1e70c
Create Date: 2025-02-12 15:33:40.284990
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'e979f6069600'
down_revision = '0dbb25a1e70c'
branch_labels = None
depends_on = None

def upgrade():
    # 1. Ajouter le nouveau champ (nullable au début car il y a des enregistrements existants)
    with op.batch_alter_table('job_offer', schema=None) as batch_op:
        batch_op.add_column(sa.Column('last_modified_by_an_employer_date', sa.DateTime(timezone=True), nullable=True))
        batch_op.alter_column('description',
                existing_type=mysql.MEDIUMTEXT(),
                type_=sa.Text(length=100000),
                existing_nullable=False)

    # 2. Mettre à jour TOUS les enregistrements existants avec la date d'exécution de la migration en UTC
    op.execute("UPDATE job_offer SET last_modified_by_an_employer_date = UTC_TIMESTAMP()")

    # 3. Rendre le champ non nullable maintenant que tous les enregistrements ont une valeur
    with op.batch_alter_table('job_offer', schema=None) as batch_op:
        batch_op.alter_column('last_modified_by_an_employer_date',
                existing_type=sa.DateTime(timezone=True),
                nullable=False)

def downgrade():
    with op.batch_alter_table('job_offer', schema=None) as batch_op:
        batch_op.alter_column('description',
                existing_type=sa.Text(length=100000),
                type_=mysql.MEDIUMTEXT(),
                existing_nullable=False)
        batch_op.drop_column('last_modified_by_an_employer_date')