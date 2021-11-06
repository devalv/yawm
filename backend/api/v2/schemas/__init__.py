# -*- coding: utf-8 -*-

from .product import ProductCreateV2Model
from .wishlist import WishlistProductsV2Model, WishlistViewV2Model
from .wishlist_products import WishlistProductUpdateV2Model, WishlistProductV2Model

__all__ = (
    "WishlistProductsV2Model",
    "WishlistViewV2Model",
    "ProductCreateV2Model",
    "WishlistProductV2Model",
    "WishlistProductUpdateV2Model",
)
