# -*- coding: utf-8 -*-
"""Wishlist rest-api handlers."""

from api.v2.schemas import WishlistProductV2Model
from fastapi import APIRouter
from pydantic import UUID4

from core.database import WishlistProductsGinoModel

basename = "wishlist-products"
wishlist_products_router = APIRouter(redirect_slashes=True, tags=[basename])


@wishlist_products_router.put(
    f"/{basename}/" + "{id}" + "/reserve",
    response_model=WishlistProductV2Model,
    status_code=201,
)
async def reserve_wishlist_product(id: UUID4):
    """API for making wishlist product reversed."""
    wishlist_product = await WishlistProductsGinoModel.get_or_404(id)
    await wishlist_product.reserve()
    return wishlist_product
