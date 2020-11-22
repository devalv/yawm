# -*- coding: utf-8 -*-
"""ORM Models for Wishlist entities."""

from uuid import uuid4

from sqlalchemy.dialects.postgresql import UUID

from . import db


class Product(db.Model):
    """Yep, it`s a Product with link to online store."""

    __tablename__ = "product"

    id = db.Column(UUID(), default=uuid4, primary_key=True)  # noqa: A003
    name = db.Column(db.Unicode(length=255), nullable=False)
    url = db.Column(db.Unicode(length=8000), nullable=False, unique=True)
    # TODO: remove unique url?
    # url = db.Column(db.Unicode(length=8000), nullable=False)
    price = db.Column(db.Numeric(precision=2), nullable=False, default=0)


class Wishlist(db.Model):
    """Wishlist is a user-bound list of Product."""

    __tablename__ = "wishlist"

    id = db.Column(UUID(), default=uuid4, primary_key=True)  # noqa: A003
    slug = db.Column(db.Unicode(length=255), nullable=False, unique=True)
    name = db.Column(db.Unicode(length=255), nullable=False)
    # user_id = db.Column()  # Foreign key to table User


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
