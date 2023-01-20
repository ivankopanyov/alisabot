"""create db

Revision ID: 280d101b18c7
Revises: 
Create Date: 2023-01-20 22:38:38.528383

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "280d101b18c7"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "position",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "service",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("description", sa.String(length=1000), nullable=False),
        sa.Column("duration", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "token_blacklist",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("token", sa.String(length=500), nullable=False),
        sa.Column("blacklisted_on", sa.DateTime(), nullable=True),
        sa.Column("expires_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("token"),
    )
    op.create_table(
        "position_service",
        sa.Column("service_id", sa.Integer(), nullable=True),
        sa.Column("position_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["position_id"],
            ["position.id"],
        ),
        sa.ForeignKeyConstraint(
            ["service_id"],
            ["service.id"],
        ),
    )
    op.create_table(
        "site_user",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("password_hash", sa.String(length=100), nullable=False),
        sa.Column("registered_on", sa.DateTime(), nullable=True),
        sa.Column("admin", sa.Boolean(), nullable=True),
        sa.Column("public_id", sa.String(length=36), nullable=True),
        sa.Column("position_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["position_id"],
            ["position.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
        sa.UniqueConstraint("public_id"),
    )
    op.create_table(
        "widget",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("info_url", sa.String(length=255), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("deadline", sa.DateTime(), nullable=True),
        sa.Column("owner_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["owner_id"],
            ["site_user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("widget")
    op.drop_table("site_user")
    op.drop_table("position_service")
    op.drop_table("token_blacklist")
    op.drop_table("service")
    op.drop_table("position")
    # ### end Alembic commands ###