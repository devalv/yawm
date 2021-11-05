# -*- coding: utf-8 -*-
"""Pydantic wishlist models (v2)."""

from typing import List

from pydantic import UUID4, BaseModel

from core.utils import BaseViewModel

from .product import ProductCreateV2Model, ProductViewV2Model


class WishlistProductsV2Model(BaseModel):
    product_urls: List[ProductCreateV2Model]


class WishlistViewV2Model(BaseViewModel):
    """Wishlist products attributes serializer."""

    name: str
    username: str
    user_id: UUID4
    products: List[ProductViewV2Model]
