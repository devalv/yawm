# -*- coding: utf-8 -*-
"""user updates

Revision ID: 39ac88efc647
Revises: 2fe62de7662f
Create Date: 2022-04-13 16:33:04.941954

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "39ac88efc647"
down_revision = "2fe62de7662f"
branch_labels = None
depends_on = None


def upgrade():
    """Apply changes on database."""
    op.drop_index(op.f("ix_user_username"), "public.user")
    op.execute("truncate public.user cascade;")
    op.add_column("user", sa.Column("password", sa.Unicode(length=255), nullable=False))
    op.create_index(op.f("ix_user_username"), "user", ["username"], unique=True)
    op.drop_constraint("user_ext_id_key", "user", type_="unique")
    op.drop_column("user", "family_name")
    op.drop_column("user", "full_name")
    op.drop_column("user", "given_name")
    op.drop_column("user", "ext_id")


def downgrade():
    """Revert changes on database."""
    op.execute("truncate public.user cascade;")
    op.add_column(
        "user",
        sa.Column("ext_id", sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    )
    op.add_column(
        "user",
        sa.Column(
            "given_name", sa.VARCHAR(length=255), autoincrement=False, nullable=True
        ),
    )
    op.add_column(
        "user",
        sa.Column(
            "full_name", sa.VARCHAR(length=255), autoincrement=False, nullable=True
        ),
    )
    op.add_column(
        "user",
        sa.Column(
            "family_name", sa.VARCHAR(length=255), autoincrement=False, nullable=True
        ),
    )
    op.create_unique_constraint("user_ext_id_key", "user", ["ext_id"])
    op.drop_column("user", "password")
    op.drop_index(op.f("ix_user_username"), "public.user")
    op.create_index(op.f("ix_user_username"), "user", ["username"], unique=False)
