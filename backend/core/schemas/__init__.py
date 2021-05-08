# -*- coding: utf-8 -*-
"""Pydantic models."""

from .product import ProductCreateModel, ProductModel, ProductUpdateModel
from .wishlist import WishlistCreateModel, WishlistModel, WishlistUpdateModel
from .wishlist_products import (
    WishlistProductsCreateModel,
    WishlistProductsModel,
    WishlistProductsUpdateModel,
)

__all__ = [
    "ProductModel",
    "ProductCreateModel",
    "ProductUpdateModel",
    "WishlistModel",
    "WishlistCreateModel",
    "WishlistUpdateModel",
    "WishlistProductsModel",
    "WishlistProductsCreateModel",
    "WishlistProductsUpdateModel",
]
