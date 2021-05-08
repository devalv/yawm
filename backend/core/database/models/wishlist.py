# -*- coding: utf-8 -*-
"""ORM Models for Wishlist entities."""

from uuid import uuid4

from asyncpg.exceptions import ForeignKeyViolationError

from sqlalchemy.dialects.postgresql import UUID

from starlette import status
from starlette.exceptions import HTTPException

from core.utils import JsonApiModel  # noqa: I100

from . import db


class Product(db.Model, JsonApiModel):
    """Yep, this is a Product with link to online store."""

    __tablename__ = "product"

    uid = db.Column(UUID(), default=uuid4, primary_key=True)
    name = db.Column(db.Unicode(length=255), nullable=False)
    url = db.Column(db.Unicode(length=8000), nullable=False, unique=True)


class Wishlist(db.Model, JsonApiModel):
    """Wishlist is a user-bound list of Product(s)."""

    __tablename__ = "wishlist"

    uid = db.Column(UUID(), default=uuid4, primary_key=True)
    name = db.Column(db.Unicode(length=255), nullable=False)

    @property
    def products(self):
        """Get products related to wishlist object."""
        return ProductWishlist.query.where(ProductWishlist.wishlist_uid == self.uid)

    # TODO: remove?
    # @property
    # def products_query(self):
    #     """Gino query for fetching wishlist-related products."""
    #     # Prepare QS for paginator
    #     paginator_fields = [  # noqa: E800
    #         Product.name,  # noqa: E800
    #         Product.url,  # noqa: E800
    #         ProductWishlist.uid,  # noqa: E800
    #         ProductWishlist.wishlist_uid,  # noqa: E800
    #         ProductWishlist.product_uid,  # noqa: E800
    #         ProductWishlist.substitutable,  # noqa: E800
    #         ProductWishlist.reserved,  # noqa: E800
    #     ]  # noqa: E800
    #     # Products <-> Wishlists relation
    #     paginator_query = db.select(paginator_fields).select_from(  # noqa: E800
    #         ProductWishlist.join(Product)  # noqa: E800
    #     )  # noqa: E800
    #     # filter Products of current Wishlist
    #     filtered_products_paginator_query = paginator_query.where(  # noqa: E800
    #         ProductWishlist.wishlist_uid == self.uid  # noqa: E800
    #     )  # noqa: E800
    #     return filtered_products_paginator_query  # noqa: E800

    async def add_product(self, product_uid: str):
        """Add existing product to wishlist."""
        try:
            rv = await ProductWishlist.create(
                product_uid=product_uid, wishlist_uid=self.uid
            )
        except ForeignKeyViolationError:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Product is not found")
        return rv


class ProductWishlist(db.Model, JsonApiModel):
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
