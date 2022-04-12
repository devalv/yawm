# -*- coding: utf-8 -*-
"""editable product name

Revision ID: 2fe62de7662f
Revises: fc713dae054e
Create Date: 2022-04-12 17:31:43.810771

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "2fe62de7662f"
down_revision = "fc713dae054e"
branch_labels = None
depends_on = None


def upgrade():
    """Apply changes on database."""
    op.add_column(
        "wishlist_products", sa.Column("name", sa.Unicode(length=255), nullable=True)
    )
    op.execute(
        """
                update
                    wishlist_products
                set
                    name = p.name
                from
                    product as p
                where
                    wishlist_products.product_id = p.id;
        """
    )
    op.alter_column(
        "wishlist_products", "name", existing_type=sa.VARCHAR(length=255), nullable=False
    )


def downgrade():
    """Revert changes on database."""
    op.drop_column("wishlist_products", "name")
