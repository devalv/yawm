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


class Wishlist(db.Model):
    """Wishlist is a user-bound list of Product(s)."""

    __tablename__ = "wishlist"

    uid = db.Column(UUID(), default=uuid4, primary_key=True)
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

    @property
    def products_query(self):
        """Gino query for fetching wishlist-related products."""
        # Prepare QS for paginator
        paginator_fields = [
            Product.name,
            Product.url,
            ProductWishlist.uid,
            ProductWishlist.wishlist_uid,
            ProductWishlist.product_uid,
            ProductWishlist.substitutable,
            ProductWishlist.reserved,
        ]
        # Products <-> Wishlists relation
        paginator_query = db.select(paginator_fields).select_from(
            ProductWishlist.join(Product)
        )
        # filter Products of current Wishlist
        filtered_products_paginator_query = paginator_query.where(
            ProductWishlist.wishlist_uid == self.uid
        )
        return filtered_products_paginator_query  # noqa: PIE781


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
    substitutable = db.Column(db.Boolean(), nullable=False, default=False)
    reserved = db.Column(db.Boolean(), nullable=False, default=False)
