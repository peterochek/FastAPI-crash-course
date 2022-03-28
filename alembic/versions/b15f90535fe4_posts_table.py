"""posts table

Revision ID: b15f90535fe4
Revises: 
Create Date: 2021-12-21 14:57:19.552311

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "b15f90535fe4"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "posts",
        sa.Column("id", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("title", sa.String(), nullable=False),
    )
    pass


def downgrade():
    op.drop_table("posts")
    pass
