# -*- coding: utf-8 -*-
"""Initial migration.

Revision ID: 85b9bef9bbee
Revises:
Create Date: 2021-05-10 13:23:59.761097

"""
from alembic import op

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "85b9bef9bbee"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    """Apply changes on database."""
    op.create_table(
        "user",
        sa.Column("id", postgresql.UUID(), nullable=False),
        sa.Column("ext_id", sa.Unicode(length=255), nullable=False),
        sa.Column("disabled", sa.Boolean(), nullable=False),
        sa.Column("superuser", sa.Boolean(), nullable=False),
        sa.Column(
            "created",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column("username", sa.Unicode(length=255), nullable=False),
        sa.Column("given_name", sa.Unicode(length=255), nullable=True),
        sa.Column("family_name", sa.Unicode(length=255), nullable=True),
        sa.Column("full_name", sa.Unicode(length=255), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("ext_id"),
    )
    op.create_index(op.f("ix_user_username"), "user", ["username"], unique=False)
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
        sa.Column("wishlist_id", postgresql.UUID(), nullable=False),
        sa.Column("product_id", postgresql.UUID(), nullable=False),
        sa.Column("substitutable", sa.Boolean(), nullable=False),
        sa.Column("reserved", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(["product_id"], ["product.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["wishlist_id"], ["wishlist.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    """Revert changes on database."""
    op.drop_index(op.f("ix_user_username"), table_name="user")
    op.drop_table("user")
    op.drop_table("wishlist_products")
    op.drop_table("wishlist")
    op.drop_table("product")
