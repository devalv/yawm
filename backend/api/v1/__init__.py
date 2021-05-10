# -*- coding: utf-8 -*-
"""Project API (version 1)."""

from .handlers import (
    product_router,
    utils_router,
    wishlist_product_router,
    wishlist_router,
)


__all__ = (
    "product_router",
    "wishlist_product_router",
    "wishlist_router",
    "utils_router",
)
