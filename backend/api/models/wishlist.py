# -*- coding: utf-8 -*-
"""ORM Models for Wishlist entities."""

from uuid import uuid4

from asyncpg.exceptions import ForeignKeyViolationError

from sqlalchemy.dialects.postgresql import UUID

from starlette import status
from starlette.exceptions import HTTPException

from . import db


class Product(db.Model):
    """Yep, this is a Product with link to online store."""

    __tablename__ = "product"

    uid = db.Column(UUID(), default=uuid4, primary_key=True)
    name = db.Column(db.Unicode(length=255), nullable=False)
    url = db.Column(db.Unicode(length=8000), nullable=False, unique=True)
    price = db.Column(db.Numeric(12, 2), nullable=False, default=0)


class Wishlist(db.Model):
    """Wishlist is a user-bound list of Product(s)."""

    __tablename__ = "wishlist"

    uid = db.Column(UUID(), default=uuid4, primary_key=True)
    slug = db.Column(db.Unicode(length=255), nullable=False, unique=True)
    name = db.Column(db.Unicode(length=255), nullable=False)

    async def add_product(self, product_uid: str):
        """Add existing product to wishlist."""
        try:
            rv = await ProductWishlist.create(
                product_uid=product_uid, wishlist_uid=self.uid
            )
        except ForeignKeyViolationError:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Product is not found")
        return rv

    async def get_products(self, paginator_limit: int, paginator_offset: int):
        """Get all related products for wishlist."""
        wishlist_products = (
            await db.select(
                [ProductWishlist.uid, Product.name, Product.price, Product.url]
            )
            .select_from(ProductWishlist.join(Product))
            .where(
                (ProductWishlist.wishlist_uid == self.uid)
                & (ProductWishlist.product_uid == Product.uid)  # noqa: W503
            )
            .limit(paginator_limit)
            .offset(paginator_offset)
            .gino.all()
        )
        return wishlist_products


class ProductWishlist(db.Model):
    """Product and Wishlist connection.

    The absence of unique together indices (product_uid, wishlist_uid) has been
    done intentionally to avoid product count.
    Example: 2 same products in 1 list should be 2 records.
    """

    __tablename__ = "product_wishlist"

    uid = db.Column(UUID(), default=uuid4, primary_key=True)
    product_uid = db.Column(UUID(), db.ForeignKey(Product.uid), nullable=False)
    wishlist_uid = db.Column(UUID(), db.ForeignKey(Wishlist.uid), nullable=False)
    reserved = db.Column(db.Boolean(), nullable=False, default=False)
