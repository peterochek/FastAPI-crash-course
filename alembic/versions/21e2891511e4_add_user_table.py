"""add user table

Revision ID: 21e2891511e4
Revises: bae7fa79a074
Create Date: 2021-12-21 15:02:45.842415

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '21e2891511e4'
down_revision = 'bae7fa79a074'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )
    pass


def downgrade():
    op.drop_table('users')
    pass
