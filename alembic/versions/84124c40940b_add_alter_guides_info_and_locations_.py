"""Add alter guides info and locations description columns

Revision ID: 84124c40940b
Revises: 6d60d05bbf42
Create Date: 2021-02-11 01:07:20.165611

"""
from alembic import op
from sqlalchemy import Text, String


# revision identifiers, used by Alembic.
revision = '84124c40940b'
down_revision = '6d60d05bbf42'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column(
        table_name="guides",
        column_name="info",
        type_=Text
    )
    op.alter_column(
        table_name="locations",
        column_name="description",
        type_=Text
    )


def downgrade():
    op.alter_column(
        table_name="guides",
        column_name="info",
        type_=String
    )
    op.alter_column(
        table_name="locations",
        column_name="description",
        type_=String
    )
