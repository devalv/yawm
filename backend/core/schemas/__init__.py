# -*- coding: utf-8 -*-
"""Pydantic models."""

from .product import (
    ProductDataCreateModel,
    ProductDataModel,
    ProductDataUpdateModel,
    ProductModel,
)
from .wishlist import (
    WishlistDataCreateModel,
    WishlistDataModel,
    WishlistDataUpdateModel,
    WishlistModel,
)
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
    "WishlistDataModel",
    "WishlistDataCreateModel",
    "WishlistDataUpdateModel",
    "WishlistProductsModel",
    "WishlistProductsCreateModel",
    "WishlistProductsUpdateModel",
]
