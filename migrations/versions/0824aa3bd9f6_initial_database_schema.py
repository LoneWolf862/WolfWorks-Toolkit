"""Initial database schema

Revision ID: 0824aa3bd9f6
Revises: 
Create Date: 2026-09-22 20:18:28.616737

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0824aa3bd9f6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "io_points",

        sa.Column(
            "id",
            sa.Integer(),
            nullable=False,
        ),

        sa.Column(
            "tag_name",
            sa.String(length=80),
            nullable=False,
        ),

        sa.Column(
            "io_type",
            sa.String(length=2),
            nullable=False,
        ),

        sa.Column(
            "address",
            sa.String(length=100),
            nullable=False,
        ),

        sa.Column(
            "description",
            sa.String(length=255),
            nullable=True,
        ),

        sa.Column(
            "signal_min",
            sa.Float(),
            nullable=True,
        ),

        sa.Column(
            "signal_max",
            sa.Float(),
            nullable=True,
        ),

        sa.Column(
            "engineering_min",
            sa.Float(),
            nullable=True,
        ),

        sa.Column(
            "engineering_max",
            sa.Float(),
            nullable=True,
        ),

        sa.Column(
            "engineering_unit",
            sa.String(length=20),
            nullable=True,
        ),

        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("address"),
        sa.UniqueConstraint("tag_name"),
    )


def downgrade():
    op.drop_table("io_points")