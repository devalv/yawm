# -*- coding: utf-8 -*-
"""Wishlist rest-api handlers."""

from api.v2.schemas import WishlistProductV2Model
from fastapi import APIRouter, Depends, Response, status
from pydantic import UUID4

from core.database import WishlistProductsGinoModel
from core.services.security import get_user_wishlist_product_gino_obj

basename = "wishlist-products"
wishlist_products_router = APIRouter(redirect_slashes=True, tags=[basename])


@wishlist_products_router.put(
    f"/{basename}/" + "{id}" + "/reserve",
    response_model=WishlistProductV2Model,
    status_code=status.HTTP_201_CREATED,
)
async def reserve_wishlist_product(id: UUID4):
    """API for making wishlist product reversed."""
    wishlist_product = await WishlistProductsGinoModel.get_or_404(id)
    await wishlist_product.reserve()
    return wishlist_product


@wishlist_products_router.delete(
    f"/{basename}/" + "{id}",
    response_class=Response,
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_wishlist_product(
    wishlist_product: WishlistProductsGinoModel = Depends(
        get_user_wishlist_product_gino_obj
    ),
):
    """API for deleting product from wishlist."""
    await wishlist_product.delete()
