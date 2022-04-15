# -*- coding: utf-8 -*-
"""Pydantic wishlist products models."""

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


class WishlistProductsUpdateModel(BaseUpdateModel):
    """Wishlist products update attributes serializer."""

    product_id: UUID4 | None
    reserved: bool | None
    substitutable: bool | None
