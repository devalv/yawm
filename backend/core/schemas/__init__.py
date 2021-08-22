# -*- coding: utf-8 -*-
"""Pydantic models."""

from .product import ProductCreateModel, ProductUpdateModel, ProductViewModel
from .security import (
    AccessToken,
    GoogleIdInfo,
    RefreshToken,
    Token,
    UserCreateModel,
    UserViewModel,
)
from .utils import ExtractUrlInModel, ExtractUrlOutModel
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
    "ExtractUrlInModel",
    "ExtractUrlOutModel",
    "UserViewModel",
    "UserCreateModel",
    "Token",
    "AccessToken",
    "RefreshToken",
    "GoogleIdInfo",
]
