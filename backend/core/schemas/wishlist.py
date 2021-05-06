# -*- coding: utf-8 -*-
"""Pydantic wishlist models."""

import uuid
from typing import Optional

from pydantic import BaseModel


class WishlistModel(BaseModel):
    """Wishlist serializer."""

    name: str
    uid: Optional[uuid.UUID] = None


class WishlistModelList(BaseModel):
    """Product list serializer."""

    name: str
    uid: uuid.UUID

    class Config:  # noqa: D106
        orm_mode = True


class ProductModel(BaseModel):
    """Product serializer."""

    name: str
    url: str
    uid: Optional[uuid.UUID] = None


class ProductModelList(BaseModel):
    """Product list serializer."""

    name: str
    uid: uuid.UUID

    class Config:  # noqa: D106
        orm_mode = True


class ProductWishlistModel(BaseModel):
    """ProductWishlist serializer."""

    wishlist_uid: uuid.UUID
    product_uid: uuid.UUID
    uid: Optional[uuid.UUID] = None
    substitutable: Optional[bool] = False
    reserved: Optional[bool] = False


class ProductWishlistModelList(BaseModel):
    """ProductWishlist list serializer."""

    product_uid: uuid.UUID
    wishlist_uid: uuid.UUID
    uid: Optional[uuid.UUID] = None
    substitutable: Optional[bool]
    reserved: Optional[bool]

    class Config:  # noqa: D106
        orm_mode = True


class AddProductWishlistModelList(BaseModel):
    """ProductWishlist list serializer."""

    product_uid: uuid.UUID
    substitutable: Optional[bool]
    reserved: Optional[bool]


class ProductWishlistUpdateModel(BaseModel):
    """ProductWishlist update serializer."""

    wishlist_uid: Optional[uuid.UUID]
    product_uid: Optional[uuid.UUID]
    reserved: Optional[bool]
    substitutable: Optional[bool]
