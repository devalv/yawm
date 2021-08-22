# -*- coding: utf-8 -*-
"""Pydantic wishlist products models."""

from typing import Optional

from pydantic import UUID4, BaseModel

from core.utils import BaseUpdateModel, BaseViewModel


class WishlistProductsCreateModel(BaseModel):
    """Wishlist products create attributes serializer."""

    product_id: UUID4
    reserved: bool
    substitutable: bool


class WishlistProductsViewModel(WishlistProductsCreateModel, BaseViewModel):
    """Wishlist products attributes serializer."""

    wishlist_id: UUID4
    product_id: UUID4
    reserved: bool
    substitutable: bool

    class Config:
        orm_mode = True


class WishlistProductsUpdateModel(WishlistProductsCreateModel, BaseUpdateModel):
    """Wishlist products update attributes serializer."""

    product_id: Optional[UUID4]
    reserved: Optional[bool]
    substitutable: Optional[bool]
