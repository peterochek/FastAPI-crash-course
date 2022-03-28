"""add content column to posts table

Revision ID: bae7fa79a074
Revises: b15f90535fe4
Create Date: 2021-12-21 15:01:56.741646

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "bae7fa79a074"
down_revision = "b15f90535fe4"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column("posts", "content")
    pass
