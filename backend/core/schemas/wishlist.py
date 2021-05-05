# -*- coding: utf-8 -*-
"""Pydantic wishlist models."""

import uuid
from typing import Optional

from pydantic import BaseModel


class WishlistModel(BaseModel):
    """Wishlist serializer."""

    name: str
    slug: str
    uid: Optional[uuid.UUID] = None


class ProductModel(BaseModel):
    """Product serializer."""

    name: str
    url: str
    uid: Optional[uuid.UUID] = None


class ProductModelOut(BaseModel):
    """Product list serializer."""

    name: str
    uid: uuid.UUID

    class Config:  # noqa: D106
        orm_mode = True


class ProductWishlistModel(BaseModel):
    """ProductWishlist serializer."""

    product_uid: uuid.UUID
    wishlist_uid: uuid.UUID
    uid: Optional[uuid.UUID] = None
    reserved: Optional[bool]


class ProductWishlistUpdateModel(BaseModel):
    """ProductWishlist update serializer."""

    product_uid: Optional[uuid.UUID]
    wishlist_uid: Optional[uuid.UUID]
    reserved: Optional[bool]


class PaginatorModel(BaseModel):
    """Query paginator serializer."""

    limit: int = 10
    offset: int = 0
