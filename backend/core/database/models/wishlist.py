# -*- coding: utf-8 -*-
"""ORM Models for Wishlist entities."""
from __future__ import annotations

import uuid
from typing import List, Optional

from asyncpg.exceptions import ForeignKeyViolationError
from pydantic import HttpUrl
from sqlalchemy.dialects.postgresql import UUID
from starlette import status
from starlette.exceptions import HTTPException

from core.database.models.security import User
from core.services import get_product_name
from core.utils.default_names import random_name

from . import BaseUpdateDateModel, db


class BaseEntityModel(BaseUpdateDateModel):
    """Base entity relation model."""

    user_id = db.Column(
        UUID(), db.ForeignKey(User.id, ondelete="CASCADE"), nullable=False
    )
    _user = None

    @property
    def user(self):  # pragma: no cover
        return self._user

    @user.setter
    def user(self, user):
        self._user = user

    @property
    def username(self):
        return self._user.username

    @classmethod
    def paginator_query(cls):
        """List of wishlists with username."""
        # TODO: @devalv ref
        q = (  # noqa: VNE001
            cls.join(User)
            .select()
            .order_by(cls.updated_at.desc(), cls.created_at.desc())
            .gino.load(cls.distinct(cls.id).load(user=User.distinct(User.id)))
        )
        return q.query

    @classmethod
    async def view_query(cls, id: uuid.UUID):
        # TODO: @devalv ref like get_or_404
        q = (  # noqa: VNE001
            cls.join(User)
            .select()
            .where(cls.id == id)
            .gino.load(cls.distinct(cls.id).load(user=User.distinct(User.id)))
        )
        return await q.first()


class Product(BaseEntityModel):
    """Yep, this is a Product with link to online store."""

    __tablename__ = "product"

    name = db.Column(db.Unicode(length=255), nullable=False)
    url = db.Column(db.Unicode(length=8000), nullable=False, unique=True)


class Wishlist(BaseEntityModel):
    """Wishlist is a user-bound list of Product(s)."""

    __tablename__ = "wishlist"

    name = db.Column(db.Unicode(length=255), nullable=False)

    @property
    def products(self):
        """Get products related to wishlist object."""
        return WishlistProducts.query.where(WishlistProducts.wishlist_id == self.id)

    @staticmethod
    async def create_product(user_id: UUID, product_url: HttpUrl) -> Product:
        # All urls should be in a lower case
        url = product_url.url.lower()
        # Search existing product
        existing_product: Product = await Product.query.where(
            Product.url == url
        ).gino.first()
        if existing_product:
            return existing_product
        product_kwargs = {"url": url, "user_id": user_id}
        # Get h1 from product page as product name
        product_name: Optional[str] = await get_product_name(product_url.url)
        if product_name:
            product_kwargs["name"] = product_name  # pragma: no cover
        else:
            product_kwargs["name"] = random_name()
        # Create new product
        new_product: Product = await Product.create(**product_kwargs)
        return new_product  # noqa: PIE781

    @classmethod
    async def create_v2(cls, user_id: UUID, product_urls: List[HttpUrl]) -> Wishlist:
        """Complex interface for WishlistV2 creation."""
        # Create new products
        created_products = set()
        for product_url in product_urls:
            created_products.add(
                await cls.create_product(user_id=user_id, product_url=product_url)
            )
        # Create new wishlist
        wishlist_name: str = random_name()
        wishlist: Wishlist = await Wishlist.create(name=wishlist_name, user_id=user_id)
        # Include products to a wishlist
        for product in created_products:
            await wishlist.add_product(product_id=product.id, product_name=product.name)
        return wishlist

    async def add_product(
        self,
        product_id: str,
        product_name: str,
        reserved: Optional[bool] = False,
        substitutable: Optional[bool] = False,
    ):
        """Add existing product to wishlist."""
        try:
            rv = await WishlistProducts.create(
                product_id=product_id,
                wishlist_id=self.id,
                name=product_name,
                reserved=reserved,
                substitutable=substitutable,
            )
        except ForeignKeyViolationError:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Product is not found")
        return rv

    async def add_products_v2(self, user_id: UUID, product_urls: List[HttpUrl]):
        """Add Products to a Wishlist."""
        # Create new products
        created_products = set()
        for product_url in product_urls:
            created_products.add(
                await self.create_product(user_id=user_id, product_url=product_url)
            )
        # Include products to a wishlist
        for product in created_products:
            await self.add_product(product_id=product.id, product_name=product.name)
        return self

    async def get_products_v2(self):
        # TODO: @devalv ref ASAP
        return (
            await WishlistProducts.join(Product)
            .join(Wishlist)
            .select()
            .where(WishlistProducts.wishlist_id == self.id)
            .gino.load(
                WishlistProducts.distinct(WishlistProducts.id).load(
                    product=Product.distinct(Product.id),
                    wishlist=Wishlist.distinct(Wishlist.id),
                )
            )
            .all()
        )


class WishlistProducts(BaseUpdateDateModel):
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
    name = db.Column(db.Unicode(length=255), nullable=False)

    _product = None
    _wishlist = None

    @property
    def product(self):
        return self._product

    @product.setter
    def product(self, product):
        self._product = product

    @property
    def wishlist(self):  # pragma: no cover
        return self._wishlist

    @wishlist.setter
    def wishlist(self, wishlist):
        self._wishlist = wishlist

    @property
    def url(self):
        return self._product.url

    async def reserve(self):
        """Mark product as `reserved`."""
        return await self.update(reserved=True).apply()
