# -*- coding: utf-8 -*-

from .product import ProductCreateModel, ProductUpdateModel, ProductViewModel
from .wishlist import WishlistUpdateModel, WishlistViewModel
from .wishlist_products import (
    WishlistProductsCreateModel,
    WishlistProductsUpdateModel,
    WishlistProductsViewModel,
)

__all__ = [
    "ProductCreateModel",
    "ProductViewModel",
    "ProductUpdateModel",
    "WishlistViewModel",
    "WishlistUpdateModel",
    "WishlistProductsViewModel",
    "WishlistProductsCreateModel",
    "WishlistProductsUpdateModel",
]
