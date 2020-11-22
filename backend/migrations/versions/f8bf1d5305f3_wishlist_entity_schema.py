# -*- coding: utf-8 -*-
"""wishlist entity schema

Revision ID: f8bf1d5305f3
Revises:
Create Date: 2020-11-22 20:19:32.938592

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "f8bf1d5305f3"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "product",
        sa.Column("id", postgresql.UUID(), nullable=False),
        sa.Column("name", sa.Unicode(length=255), nullable=False),
        sa.Column("url", sa.Unicode(length=8000), nullable=False),
        sa.Column("price", sa.Numeric(precision=2), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("url"),
    )
    op.create_table(
        "wishlist",
        sa.Column("id", postgresql.UUID(), nullable=False),
        sa.Column("slug", sa.Unicode(length=255), nullable=False),
        sa.Column("name", sa.Unicode(length=255), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("slug"),
    )
    op.create_table(
        "product_wishlist",
        sa.Column("id", postgresql.UUID(), nullable=False),
        sa.Column("product_id", postgresql.UUID(), nullable=False),
        sa.Column("wishlist_id", postgresql.UUID(), nullable=False),
        sa.Column("reserved", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(["product_id"], ["product.id"]),
        sa.ForeignKeyConstraint(["wishlist_id"], ["wishlist.id"]),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    op.drop_table("product_wishlist")
    op.drop_table("wishlist")
    op.drop_table("product")
