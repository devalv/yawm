# -*- coding: utf-8 -*-
"""Project API (version 1)."""

from .handlers import (
    auth_router,
    product_router,
    security_router,
    utils_router,
    wishlist_product_router,
    wishlist_router,
)

__all__ = (
    "auth_router",
    "product_router",
    "wishlist_product_router",
    "wishlist_router",
    "utils_router",
    "security_router",
)
