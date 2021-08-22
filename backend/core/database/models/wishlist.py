# -*- coding: utf-8 -*-
"""ORM Models for Wishlist entities."""

from asyncpg.exceptions import ForeignKeyViolationError
from sqlalchemy.dialects.postgresql import UUID
from starlette import status
from starlette.exceptions import HTTPException

from core.database.models.security import User

from . import AbstractUpdateDateModel, db


class Product(AbstractUpdateDateModel):
    """Yep, this is a Product with link to online store."""

    __tablename__ = "product"

    name = db.Column(db.Unicode(length=255), nullable=False)
    url = db.Column(db.Unicode(length=8000), nullable=False, unique=True)
    user_id = db.Column(
        UUID(), db.ForeignKey(User.id, ondelete="CASCADE"), nullable=False
    )


class Wishlist(AbstractUpdateDateModel):
    """Wishlist is a user-bound list of Product(s)."""

    __tablename__ = "wishlist"

    name = db.Column(db.Unicode(length=255), nullable=False)
    user_id = db.Column(
        UUID(), db.ForeignKey(User.id, ondelete="CASCADE"), nullable=False
    )

    @classmethod
    def paginator_list(cls):
        # TODO: @devalv ref
        q = db.select([cls, User.username]).select_from(cls.join(User))  # noqa: VNE001
        loaded = q.gino.load((cls, User))
        return loaded.query

    @property
    def products(self):
        """Get products related to wishlist object."""
        return WishlistProducts.query.where(WishlistProducts.wishlist_id == self.id)

    async def add_product(self, product_id: str, reserved: bool, substitutable: bool):
        """Add existing product to wishlist."""
        try:
            rv = await WishlistProducts.create(
                product_id=product_id,
                wishlist_id=self.id,
                reserved=reserved,
                substitutable=substitutable,
            )
        except ForeignKeyViolationError:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Product is not found")
        return rv


class WishlistProducts(AbstractUpdateDateModel):
    """Product related to Wishlist connection.

    The absence of unique together indices (product_id, wishlist_id) has been
    done intentionally to avoid product count.
    Example: 2 same products in 1 list should be 2 records.
    """

    __tablename__ = "wishlist_products"

    wishlist_id = db.Column(
        UUID(), db.ForeignKey(Wishlist.id, ondelete="CASCADE"), nullable=False
    )
    product_id = db.Column(
        UUID(), db.ForeignKey(Product.id, ondelete="CASCADE"), nullable=False
    )
    substitutable = db.Column(db.Boolean(), nullable=False, default=False)
    reserved = db.Column(db.Boolean(), nullable=False, default=False)
