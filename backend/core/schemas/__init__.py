# -*- coding: utf-8 -*-
"""Pydantic models."""

from .product import (
    ProductDataCreateModel,
    ProductDataModel,
    ProductDataUpdateModel,
    ProductModel,
)
from .security import Token, TokenData, UserDBModel
from .utils import ExtractUrlDataInModel, ExtractUrlModelDataOutModel
from .wishlist import (
    WishlistDataCreateModel,
    WishlistDataModel,
    WishlistDataUpdateModel,
    WishlistModel,
)
from .wishlist_products import (
    WishlistProductsDataCreateModel,
    WishlistProductsDataModel,
    WishlistProductsDataUpdateModel,
    WishlistProductsModel,
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
    "WishlistProductsDataModel",
    "WishlistProductsDataCreateModel",
    "WishlistProductsDataUpdateModel",
    "ExtractUrlModelDataOutModel",
    "ExtractUrlDataInModel",
    "UserDBModel",
    "Token",
    "TokenData",
]
