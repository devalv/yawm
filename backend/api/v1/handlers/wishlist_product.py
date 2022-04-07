# -*- coding: utf-8 -*-
"""Wishlist rest-api handlers."""

from fastapi import APIRouter, Depends, Response, status
from fastapi_pagination.ext.gino import paginate
from fastapi_pagination.links import Page
from pydantic import UUID4

from api.v1.schemas import (
    WishlistProductsCreateModel,
    WishlistProductsUpdateModel,
    WishlistProductsViewModel,
)
from core.database import WishlistGinoModel, WishlistProductsGinoModel
from core.services.security import get_user_wishlist_gino_obj, get_wishlist_gino_obj

wishlist_product_router = APIRouter(redirect_slashes=True, tags=["wishlist-products"])


@wishlist_product_router.get(
    "/wishlist/{id}/products",
    response_model=Page[WishlistProductsViewModel],
    deprecated=True,
)
async def list_wishlist_products(
    wishlist: WishlistGinoModel = Depends(get_wishlist_gino_obj),
):
    """API for getting all related products."""
    return await paginate(wishlist.products)


@wishlist_product_router.post(
    "/wishlist/{id}/products", response_model=WishlistProductsViewModel, deprecated=True
)
async def create_wishlist_product(
    product: WishlistProductsCreateModel,
    wishlist: WishlistGinoModel = Depends(get_user_wishlist_gino_obj),
):
    """API for adding existing product to a existing wishlist."""
    return await wishlist.add_product(**product.dict())


@wishlist_product_router.put(
    "/wishlist/{id}/products/{pw_id}",
    response_model=WishlistProductsViewModel,
    deprecated=True,
)
async def update_wishlist_product(
    pw_id: UUID4,
    pwm: WishlistProductsUpdateModel,
    wishlist: WishlistGinoModel = Depends(get_user_wishlist_gino_obj),
):
    """API for updating product associated to a wishlist."""
    wishlist_product = await WishlistProductsGinoModel.get_or_404(pw_id)
    await wishlist_product.update(**pwm.non_null_dict).apply()
    return wishlist_product


@wishlist_product_router.put(
    "/wishlist/{id}/products/{pw_id}/reserve",
    response_model=WishlistProductsViewModel,
    deprecated=True,
)
async def reserve_wishlist_product(pw_id: UUID4, pwm: WishlistProductsUpdateModel):
    """API for updating product associated to a wishlist."""
    wishlist_product = await WishlistProductsGinoModel.get_or_404(pw_id)
    await wishlist_product.update(**pwm.non_null_dict).apply()
    return wishlist_product


@wishlist_product_router.delete(
    "/wishlist/{id}/products/{pw_id}",
    response_class=Response,
    status_code=status.HTTP_204_NO_CONTENT,
    deprecated=True,
)
async def delete_wishlist_product(
    pw_id: UUID4,
    wishlist: WishlistGinoModel = Depends(get_user_wishlist_gino_obj),
):
    """API for removing product from wishlist."""
    wishlist_product = await WishlistProductsGinoModel.get_or_404(pw_id)
    await wishlist_product.delete()
