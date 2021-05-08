# -*- coding: utf-8 -*-
"""Pydantic wishlist models."""

import uuid
from typing import Optional

from pydantic import BaseModel


class WishlistBaseModel(BaseModel):  # noqa: D101
    id: Optional[uuid.UUID] = None  # noqa: A002, A003, VNE003
    type: str  # noqa: A003, VNE003


class WishlistModel(BaseModel):
    """Wishlist serializer."""

    name: str
    id: Optional[uuid.UUID] = None  # noqa: A002, A003, VNE003


class WishlistAttributesModel(BaseModel):  # noqa: D101
    name: str


class WishlistModelList(WishlistBaseModel):
    """Product list serializer."""

    attributes: WishlistAttributesModel

    class Config:  # noqa: D106
        orm_mode = True


class ProductModel(BaseModel):
    """Product serializer."""

    name: str
    url: str
    id: Optional[uuid.UUID] = None  # noqa: A002, A003, VNE003


class ProductBaseModel(BaseModel):  # noqa: D101
    id: Optional[uuid.UUID] = None  # noqa: A002, A003, VNE003
    type: str  # noqa: A002, A003, VNE003


class ProductAttributesModel(BaseModel):  # noqa: D101
    name: str


class ProductModelList(ProductBaseModel):
    """Product list serializer."""

    attributes: ProductAttributesModel

    class Config:  # noqa: D106
        orm_mode = True


class ProductWishlistModel(BaseModel):
    """ProductWishlist serializer."""

    wishlist_id: uuid.UUID
    product_id: uuid.UUID
    id: Optional[uuid.UUID] = None  # noqa: A002, A003, VNE003
    substitutable: Optional[bool] = False
    reserved: Optional[bool] = False


class ProductWishlistBaseModel(BaseModel):  # noqa: D101
    id: Optional[uuid.UUID]  # noqa: A002, A003, VNE003
    type: str  # noqa: A003, VNE003


class ProductWishlistAttributesModel(BaseModel):  # noqa: D101
    product_id: uuid.UUID
    wishlist_id: uuid.UUID
    substitutable: Optional[bool]
    reserved: Optional[bool]

    class Config:  # noqa: D106
        orm_mode = True


class ProductWishlistModelList(ProductBaseModel):
    """Product list serializer."""

    attributes: ProductWishlistAttributesModel

    class Config:  # noqa: D106
        orm_mode = True


class AddProductWishlistModel(BaseModel):
    """ProductWishlist list serializer."""

    product_id: uuid.UUID
    substitutable: Optional[bool]
    reserved: Optional[bool]


class ProductWishlistUpdateModel(BaseModel):
    """ProductWishlist update serializer."""

    wishlist_id: Optional[uuid.UUID]
    product_id: Optional[uuid.UUID]
    reserved: Optional[bool]
    substitutable: Optional[bool]
