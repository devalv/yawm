# -*- coding: utf-8 -*-

from .product import ProductCreateV2Model
from .wishlist import WishlistCreateV2Model, WishlistViewV2Model
from .wishlist_products import WishlistProductV2Model

__all__ = (
    "WishlistCreateV2Model",
    "WishlistViewV2Model",
    "ProductCreateV2Model",
    "WishlistProductV2Model",
)
