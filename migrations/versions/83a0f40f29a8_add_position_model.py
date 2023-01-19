"""add position model

Revision ID: 83a0f40f29a8
Revises: 5926df22a7cf
Create Date: 2023-01-16 14:00:49.580388

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "83a0f40f29a8"
down_revision = "5926df22a7cf"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "position",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("owner_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["owner_id"],
            ["site_user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("position")
    # ### end Alembic commands ###
