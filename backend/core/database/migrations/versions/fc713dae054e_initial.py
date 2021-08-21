# -*- coding: utf-8 -*-
"""Initial migration.

Revision ID: fc713dae054e
Revises:
Create Date: 2021-08-21 19:41:56.255256

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "fc713dae054e"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    """Apply changes on database."""
    op.create_table(
        "user",
        sa.Column("ext_id", sa.Unicode(length=255), nullable=False),
        sa.Column("disabled", sa.Boolean(), nullable=False),
        sa.Column("superuser", sa.Boolean(), nullable=False),
        sa.Column("username", sa.Unicode(length=255), nullable=False),
        sa.Column("given_name", sa.Unicode(length=255), nullable=True),
        sa.Column("family_name", sa.Unicode(length=255), nullable=True),
        sa.Column("full_name", sa.Unicode(length=255), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column("id", postgresql.UUID(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("ext_id"),
    )
    op.create_index(op.f("ix_user_username"), "user", ["username"], unique=False)
    op.create_table(
        "product",
        sa.Column("name", sa.Unicode(length=255), nullable=False),
        sa.Column("url", sa.Unicode(length=8000), nullable=False),
        sa.Column("user_id", postgresql.UUID(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column("id", postgresql.UUID(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["user.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("url"),
    )
    op.create_table(
        "token_info",
        sa.Column("user_id", postgresql.UUID(), nullable=False),
        sa.Column("refresh_token", sa.Unicode(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["user_id"], ["user.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("user_id"),
    )
    op.create_index(
        op.f("ix_token_info_refresh_token"),
        "token_info",
        ["refresh_token"],
        unique=False,
    )
    op.create_table(
        "wishlist",
        sa.Column("name", sa.Unicode(length=255), nullable=False),
        sa.Column("user_id", postgresql.UUID(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column("id", postgresql.UUID(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["user.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "wishlist_products",
        sa.Column("wishlist_id", postgresql.UUID(), nullable=False),
        sa.Column("product_id", postgresql.UUID(), nullable=False),
        sa.Column("substitutable", sa.Boolean(), nullable=False),
        sa.Column("reserved", sa.Boolean(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column("id", postgresql.UUID(), nullable=False),
        sa.ForeignKeyConstraint(["product_id"], ["product.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["wishlist_id"], ["wishlist.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    """Revert changes on database."""
    op.drop_table("wishlist_products")
    op.drop_table("wishlist")
    op.drop_index(op.f("ix_token_info_refresh_token"), table_name="token_info")
    op.drop_table("token_info")
    op.drop_table("product")
    op.drop_index(op.f("ix_user_username"), table_name="user")
    op.drop_table("user")
