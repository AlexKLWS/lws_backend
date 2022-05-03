"""update secret column with false default

Revision ID: 97bbfe39e0af
Revises: 9483480e8a35
Create Date: 2022-05-03 18:57:27.135449

"""
import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision = '97bbfe39e0af'
down_revision = '9483480e8a35'
branch_labels = None
depends_on = None


def upgrade():
    op.execute('UPDATE ext_materials SET secret = FALSE WHERE secret IS NULL')
    op.execute('UPDATE articles SET secret = FALSE WHERE secret IS NULL')
    op.execute('UPDATE guides SET secret = FALSE WHERE secret IS NULL')

    op.alter_column(
        table_name="ext_materials",
        column_name="secret",
        nullable=False,
    )
    op.alter_column(
        table_name="articles",
        column_name="secret",
        nullable=False,
    )
    op.alter_column(
        table_name="guides",
        column_name="secret",
        nullable=False,
    )


def downgrade():
    op.alter_column(
        table_name="ext_materials",
        column_name="secret",
        nullable=True,
    )
    op.alter_column(
        table_name="articles",
        column_name="secret",
        nullable=True,
    )
    op.alter_column(
        table_name="guides",
        column_name="secret",
        nullable=True,
    )
    op.execute('UPDATE ext_materials SET secret = NULL WHERE secret IS FALSE')
    op.execute('UPDATE articles SET secret = NULL WHERE secret IS FALSE')
    op.execute('UPDATE guides SET secret = NULL WHERE secret IS FALSE')
