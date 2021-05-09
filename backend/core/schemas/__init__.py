# -*- coding: utf-8 -*-
"""Pydantic models."""

from .product import (
    ProductDataCreateModel,
    ProductDataModel,
    ProductDataUpdateModel,
    ProductModel,
)
from .wishlist import WishlistCreateModel, WishlistModel, WishlistUpdateModel
from .wishlist_products import (
    WishlistProductsCreateModel,
    WishlistProductsModel,
    WishlistProductsUpdateModel,
)

__all__ = [
    "ProductModel",
    "ProductDataCreateModel",
    "ProductDataUpdateModel",
    "ProductDataModel",
    "WishlistModel",
    "WishlistCreateModel",
    "WishlistUpdateModel",
    "WishlistProductsModel",
    "WishlistProductsCreateModel",
    "WishlistProductsUpdateModel",
]
