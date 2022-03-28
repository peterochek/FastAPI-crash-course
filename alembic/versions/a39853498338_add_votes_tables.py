"""add votes tables

Revision ID: a39853498338
Revises: 850a5ece90e9
Create Date: 2021-12-21 15:07:55.374482

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "a39853498338"
down_revision = "850a5ece90e9"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "votes",
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("post_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["post_id"], ["posts.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("user_id", "post_id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("votes")
    # ### end Alembic commands ###
