# -*- coding: utf-8 -*-
"""Wishlist rest-api handlers."""

from .auth import auth_router
from .product import product_router
from .security import security_router
from .utils import utils_router
from .wishlist import wishlist_router
from .wishlist_product import wishlist_product_router

__all__ = (
    "auth_router",
    "product_router",
    "wishlist_product_router",
    "wishlist_router",
    "utils_router",
    "security_router",
)
