# -*- coding: utf-8 -*-
"""Project database configuration."""

from .models import db
from .models.wishlist import Product as ProductGinoModel, Wishlist as WishlistGinoModel

__all__ = ["ProductGinoModel", "WishlistGinoModel", "db"]