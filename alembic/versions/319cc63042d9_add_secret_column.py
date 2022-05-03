"""add secret column

Revision ID: 319cc63042d9
Revises: 84124c40940b
Create Date: 2022-05-02 00:46:05.438286

"""
from alembic import op
from sqlalchemy import Boolean
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '319cc63042d9'
down_revision = '84124c40940b'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("articles", sa.Column("secret", Boolean))
    op.add_column("guides", sa.Column("secret", Boolean))


def downgrade():
    op.drop_column("articles", "secret")
    op.drop_column("guides", "secret")
