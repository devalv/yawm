# -*- coding: utf-8 -*-
"""Project database configuration."""

from .models import db
from .models.security import TokenInfo as TokenInfoGinoModel
from .models.security import User as UserGinoModel
from .models.wishlist import Product as ProductGinoModel
from .models.wishlist import Wishlist as WishlistGinoModel

__all__ = [
    "ProductGinoModel",
    "WishlistGinoModel",
    "UserGinoModel",
    "TokenInfoGinoModel",
    "db",
]
