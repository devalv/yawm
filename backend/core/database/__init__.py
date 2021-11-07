# -*- coding: utf-8 -*-
"""Project database configuration."""

from .models import db, is_database_online
from .models.security import TokenInfo as TokenInfoGinoModel
from .models.security import User as UserGinoModel
from .models.wishlist import Product as ProductGinoModel
from .models.wishlist import Wishlist as WishlistGinoModel
from .models.wishlist import WishlistProducts as WishlistProductsGinoModel

__all__ = [
    "ProductGinoModel",
    "WishlistProductsGinoModel",
    "WishlistGinoModel",
    "UserGinoModel",
    "TokenInfoGinoModel",
    "db",
    "is_database_online",
]
