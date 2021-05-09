# -*- coding: utf-8 -*-
"""Pydantic models."""

from .product import (
    ProductCreateModel,
    ProductDataModel,
    ProductModel,
    ProductUpdateModel,
)
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
    "ProductDataModel",
    "WishlistModel",
    "WishlistCreateModel",
    "WishlistUpdateModel",
    "WishlistProductsModel",
    "WishlistProductsCreateModel",
    "WishlistProductsUpdateModel",
]
