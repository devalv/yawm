# -*- coding: utf-8 -*-
"""ORM Models for Wishlist entities."""

from uuid import uuid4

from asyncpg.exceptions import ForeignKeyViolationError

from sqlalchemy.dialects.postgresql import UUID

from starlette import status
from starlette.exceptions import HTTPException

from core.utils import JsonApiGinoModel  # noqa: I100

from . import db


class Product(db.Model, JsonApiGinoModel):
    """Yep, this is a Product with link to online store."""

    __tablename__ = "product"

    id = db.Column(UUID(), default=uuid4, primary_key=True)  # noqa: A002, A003, VNE003
    name = db.Column(db.Unicode(length=255), nullable=False)
    url = db.Column(db.Unicode(length=8000), nullable=False, unique=True)


class Wishlist(db.Model, JsonApiGinoModel):
    """Wishlist is a user-bound list of Product(s)."""

    __tablename__ = "wishlist"

    id = db.Column(UUID(), default=uuid4, primary_key=True)  # noqa: A002, A003, VNE003
    name = db.Column(db.Unicode(length=255), nullable=False)

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


class WishlistProducts(db.Model, JsonApiGinoModel):
    """Product related to Wishlist connection.

    The absence of unique together indices (product_id, wishlist_id) has been
    done intentionally to avoid product count.
    Example: 2 same products in 1 list should be 2 records.
    """

    __tablename__ = "wishlist_products"

    id = db.Column(UUID(), default=uuid4, primary_key=True)  # noqa: A002, A003, VNE003
    wishlist_id = db.Column(
        UUID(), db.ForeignKey(Wishlist.id, ondelete="CASCADE"), nullable=False
    )
    product_id = db.Column(
        UUID(), db.ForeignKey(Product.id, ondelete="CASCADE"), nullable=False
    )
    substitutable = db.Column(db.Boolean(), nullable=False, default=False)
    reserved = db.Column(db.Boolean(), nullable=False, default=False)
