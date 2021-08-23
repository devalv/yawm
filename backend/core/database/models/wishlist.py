# -*- coding: utf-8 -*-
"""ORM Models for Wishlist entities."""
import uuid

from asyncpg.exceptions import ForeignKeyViolationError
from sqlalchemy.dialects.postgresql import UUID
from starlette import status
from starlette.exceptions import HTTPException

from core.database.models.security import User

from . import BaseUpdateDateModel, db


class BaseEntityModel(BaseUpdateDateModel):
    """Base entity relation model."""

    user_id = db.Column(
        UUID(), db.ForeignKey(User.id, ondelete="CASCADE"), nullable=False
    )

    def __init__(self, **values):
        super().__init__(**values)
        self._user = None

    @property
    def user(self):
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
    async def view_query(cls, id: uuid.UUID):  # noqa: A002
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
