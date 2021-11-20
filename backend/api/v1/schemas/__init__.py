# -*- coding: utf-8 -*-

from .product import ProductCreateModel, ProductUpdateModel, ProductViewModel
from .wishlist import WishlistCreateModel, WishlistUpdateModel, WishlistViewModel
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
    "WishlistCreateModel",
    "WishlistUpdateModel",
    "WishlistProductsViewModel",
    "WishlistProductsCreateModel",
    "WishlistProductsUpdateModel",
]
