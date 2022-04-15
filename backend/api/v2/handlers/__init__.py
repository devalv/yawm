# -*- coding: utf-8 -*-
"""Wishlist rest-api handlers (V2)."""

from .security import local_security_router
from .wishlist import wishlist_router
from .wishlist_product import wishlist_products_router

__all__ = ("wishlist_router", "wishlist_products_router", "local_security_router")
