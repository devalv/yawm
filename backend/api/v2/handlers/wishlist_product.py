# -*- coding: utf-8 -*-
"""Wishlist rest-api handlers."""

from api.v2.schemas import WishlistProductUpdateV2Model, WishlistProductV2Model
from fastapi import APIRouter, Depends, Response, status

from core.database import WishlistProductsGinoModel
from core.services.security import (
    get_user_wishlist_product_gino_obj,
    get_wishlist_product_gino_obj,
)

basename = "wishlist-products"
wishlist_products_router = APIRouter(redirect_slashes=True, tags=[basename])


@wishlist_products_router.put(
    f"/{basename}/" + "{id}" + "/reserve",
    response_model=WishlistProductV2Model,
    status_code=status.HTTP_201_CREATED,
)
async def reserve_wishlist_product(
    wishlist_product: WishlistProductsGinoModel = Depends(get_wishlist_product_gino_obj),
):
    """API for making wishlist product reversed."""
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


@wishlist_products_router.put(
    f"/{basename}/" + "{id}",
    response_model=WishlistProductV2Model,
)
async def update_wishlist_product(
    wpm: WishlistProductUpdateV2Model,
    wishlist_product: WishlistProductsGinoModel = Depends(
        get_user_wishlist_product_gino_obj
    ),
):
    """API for updating WishlistProduct attributes."""
    await wishlist_product.update(**wpm.dict()).apply()
    return wishlist_product
