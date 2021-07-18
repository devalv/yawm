# -*- coding: utf-8 -*-
"""Wishlist rest-api handlers."""

from fastapi import APIRouter, Depends, Response, status
from fastapi_pagination.ext.gino import paginate
from fastapi_versioning import version
from pydantic import UUID4

from core.database import WishlistGinoModel
from core.database.models.wishlist import WishlistProducts
from core.schemas import (
    WishlistProductsDataCreateModel,
    WishlistProductsDataModel,
    WishlistProductsDataUpdateModel,
    WishlistProductsModel,
)
from core.services.security import get_user_wishlist, get_wishlist
from core.utils import JsonApiPage

wishlist_product_router = APIRouter(redirect_slashes=True, tags=["wishlist-products"])


@wishlist_product_router.get(
    "/wishlist/{id}/products", response_model=JsonApiPage[WishlistProductsModel]
)
@version(1)
async def list_wishlist_products(
    wishlist: WishlistGinoModel = Depends(get_wishlist),  # noqa: B008
):
    """API for getting all related products."""
    return await paginate(wishlist.products)


@wishlist_product_router.post(
    "/wishlist/{id}/products", response_model=WishlistProductsDataModel
)
@version(1)
async def create_wishlist_product(
    product: WishlistProductsDataCreateModel,
    wishlist: WishlistGinoModel = Depends(get_user_wishlist),  # noqa: B008
):
    """API for adding existing product to a existing wishlist."""
    return await wishlist.add_product(**product.data.validated_attributes)


@wishlist_product_router.put(
    "/wishlist/{id}/products/{pw_id}", response_model=WishlistProductsDataModel
)
@version(1)
async def update_wishlist_product(
    pw_id: UUID4,
    pwm: WishlistProductsDataUpdateModel,
    wishlist: WishlistGinoModel = Depends(get_user_wishlist),  # noqa: B008
):
    """API for updating product associated to a wishlist."""
    wishlist_product = await WishlistProducts.get_or_404(pw_id)
    await wishlist_product.update(**pwm.data.non_null_attributes).apply()
    return wishlist_product


@wishlist_product_router.delete(
    "/wishlist/{id}/products/{pw_id}",
    response_class=Response,
    status_code=status.HTTP_204_NO_CONTENT,
)
@version(1)
async def delete_wishlist_product(
    pw_id: UUID4, wishlist: WishlistGinoModel = Depends(get_user_wishlist)  # noqa: B008
):
    """API for removing product from wishlist."""
    wishlist_product = await WishlistProducts.get_or_404(pw_id)
    await wishlist_product.delete()
