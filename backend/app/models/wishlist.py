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

    id = db.Column(UUID(), default=uuid4, primary_key=True)  # noqa: A003
    name = db.Column(db.Unicode(length=255), nullable=False)
    url = db.Column(db.Unicode(length=8000), nullable=False, unique=True)
    price = db.Column(db.Numeric(12, 2), nullable=False, default=0)


class Wishlist(db.Model):
    """Wishlist is a user-bound list of Product(s)."""

    __tablename__ = "wishlist"

    id = db.Column(UUID(), default=uuid4, primary_key=True)  # noqa: A003
    slug = db.Column(db.Unicode(length=255), nullable=False, unique=True)
    name = db.Column(db.Unicode(length=255), nullable=False)

    async def add_product(self, product_id: str):
        """Add existing product to wishlist."""
        try:
            rv = await ProductWishlist.create(
                product_id=product_id, wishlist_id=self.id
            )
        except ForeignKeyViolationError:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Product is not found")
        return rv

    async def remove_product(self, product_id: str):
        """Remove existing product from wishlist."""
        rv = await ProductWishlist.query.where(
            (ProductWishlist.product_id == product_id)
            & (ProductWishlist.wishlist_id == self.id)  # noqa
        ).gino.first()
        if not rv:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Record is not found")
        await rv.delete()
        return rv

    async def get_products(self):
        """Get all related products for wishlist."""
        products = (
            await Product.join(
                ProductWishlist.query.where(
                    ProductWishlist.wishlist_id == self.id
                ).alias()
            )
            .select()
            .gino.load(Product)
            .all()
        )
        return [product.to_dict() for product in products]


class ProductWishlist(db.Model):
    """Product and Wishlist connection.

    The absence of unique together indices (product_id, wishlist_id) has been
    done intentionally to avoid product count.
    """

    __tablename__ = "product_wishlist"

    id = db.Column(UUID(), default=uuid4, primary_key=True)  # noqa: A003
    product_id = db.Column(UUID(), db.ForeignKey(Product.id), nullable=False)
    wishlist_id = db.Column(UUID(), db.ForeignKey(Wishlist.id), nullable=False)
    reserved = db.Column(db.Boolean(), nullable=False, default=False)
