"""update position model

Revision ID: 43424e09bc34
Revises: 5e75f29613ee
Create Date: 2023-01-16 14:29:20.800241

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "43424e09bc34"
down_revision = "5e75f29613ee"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
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
    op.drop_table("services")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "services",
        sa.Column("service_id", sa.INTEGER(), nullable=True),
        sa.Column("position_id", sa.INTEGER(), nullable=True),
        sa.ForeignKeyConstraint(
            ["position_id"],
            ["position.id"],
        ),
        sa.ForeignKeyConstraint(
            ["service_id"],
            ["service.id"],
        ),
    )
    op.drop_table("position_service")
    # ### end Alembic commands ###
