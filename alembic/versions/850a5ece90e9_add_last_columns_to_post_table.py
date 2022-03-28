"""add last columns to post table

Revision ID: 850a5ece90e9
Revises: 4adb82b23872
Create Date: 2021-12-21 15:05:07.834893

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "850a5ece90e9"
down_revision = "4adb82b23872"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "posts",
        sa.Column("published", sa.Boolean(), nullable=False, server_default="TRUE"),
    )
    op.add_column(
        "posts",
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("NOW()"),
        ),
    )
    pass


def downgrade():
    op.drop_column("posts", "published")
    op.drop_column("posts", "created_at")
    pass
