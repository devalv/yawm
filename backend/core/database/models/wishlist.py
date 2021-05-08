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
        return ProductWishlist.query.where(ProductWishlist.wishlist_id == self.id)

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

    async def add_product(self, product_id: str):
        """Add existing product to wishlist."""
        try:
            rv = await ProductWishlist.create(
                product_id=product_id, wishlist_id=self.id
            )
        except ForeignKeyViolationError:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Product is not found")
        return rv


class ProductWishlist(db.Model, JsonApiGinoModel):
    """Product and Wishlist connection.

    The absence of unique together indices (product_id, wishlist_id) has been
    done intentionally to avoid product count.
    Example: 2 same products in 1 list should be 2 records.
    """

    __tablename__ = "product_wishlist"

    id = db.Column(UUID(), default=uuid4, primary_key=True)  # noqa: A002, A003, VNE003
    product_id = db.Column(UUID(), db.ForeignKey(Product.id), nullable=False)
    wishlist_id = db.Column(UUID(), db.ForeignKey(Wishlist.id), nullable=False)
    substitutable = db.Column(db.Boolean(), nullable=False, default=False)
    reserved = db.Column(db.Boolean(), nullable=False, default=False)
