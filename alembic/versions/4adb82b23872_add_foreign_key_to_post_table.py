"""add foreign key to post table

Revision ID: 4adb82b23872
Revises: 21e2891511e4
Create Date: 2021-12-21 15:04:24.044553

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4adb82b23872'
down_revision = '21e2891511e4'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table="posts", referent_table="users", local_cols=[
                          'owner_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade():
    op.drop_constraint('post_users_fk', table_name="posts")
    op.drop_column('posts', 'owner_id')
    pass
