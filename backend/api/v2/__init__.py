# -*- coding: utf-8 -*-
"""Project API (version 2)."""

from .handlers import local_security_router, wishlist_products_router, wishlist_router

__all__ = ("wishlist_router", "wishlist_products_router", "local_security_router")
