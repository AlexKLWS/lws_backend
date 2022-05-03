"""add secret column to ext_materials

Revision ID: 9483480e8a35
Revises: 319cc63042d9
Create Date: 2022-05-03 16:02:29.574874

"""
from alembic import op
from sqlalchemy import Boolean
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9483480e8a35'
down_revision = '319cc63042d9'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("ext_materials", sa.Column("secret", Boolean))


def downgrade():
    op.drop_column("ext_materials", "secret")
