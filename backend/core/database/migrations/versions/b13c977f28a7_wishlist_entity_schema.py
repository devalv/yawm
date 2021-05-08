# -*- coding: utf-8 -*-
"""wishlist entity schema.

Revision ID: b13c977f28a7
Revises:
Create Date: 2020-11-22 21:09:32.838798

"""
from alembic import op

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "b13c977f28a7"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    """Apply changes on database."""
    op.create_table(
        "product",
        sa.Column("id", postgresql.UUID(), nullable=False),
        sa.Column("name", sa.Unicode(length=255), nullable=False),
        sa.Column("url", sa.Unicode(length=8000), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("url"),
    )
    op.create_table(
        "wishlist",
        sa.Column("id", postgresql.UUID(), nullable=False),
        sa.Column("name", sa.Unicode(length=255), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "wishlist_products",
        sa.Column("id", postgresql.UUID(), nullable=False),
        sa.Column("product_id", postgresql.UUID(), nullable=False),
        sa.Column("wishlist_id", postgresql.UUID(), nullable=False),
        sa.Column("reserved", sa.Boolean(), nullable=False),
        sa.Column("substitutable", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(["product_id"], ["product.id"]),
        sa.ForeignKeyConstraint(["wishlist_id"], ["wishlist.id"]),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    """Revert changes on database."""
    op.drop_table("wishlist_products")
    op.drop_table("wishlist")
    op.drop_table("product")
