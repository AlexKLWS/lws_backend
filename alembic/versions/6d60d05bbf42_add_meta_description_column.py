"""Add meta description column

Revision ID: 6d60d05bbf42
Revises: 
Create Date: 2021-02-11 00:01:40.656972

"""
from alembic import op
from sqlalchemy import Text
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6d60d05bbf42'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("articles", sa.Column("meta_description", Text))
    op.add_column("guides", sa.Column("meta_description", Text))


def downgrade():
    op.drop_column("articles", "meta_description")
    op.drop_column("guides", "meta_description")
