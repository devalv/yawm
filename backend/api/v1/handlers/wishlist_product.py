# -*- coding: utf-8 -*-
"""Wishlist rest-api handlers."""

from fastapi import APIRouter, Response, status

from fastapi_pagination.ext.gino import paginate

from pydantic import UUID4

from core.database.models.wishlist import Wishlist, WishlistProducts  # noqa: I100
from core.schemas import (  # noqa: I100
    WishlistProductsDataCreateModel,
    WishlistProductsDataModel,
    WishlistProductsDataUpdateModel,
    WishlistProductsModel,
)
from core.utils import JsonApiPage  # noqa: I100

wishlist_product_router = APIRouter(
    prefix="/api/v1", redirect_slashes=True, tags=["wishlist-products"]
)


@wishlist_product_router.get(
    "/wishlist/{id}/products", response_model=JsonApiPage[WishlistProductsModel]
)
async def list_wishlist_products(id: UUID4):  # noqa: A002
    """API for getting all related products."""
    wishlist = await Wishlist.get_or_404(id)
    return await paginate(wishlist.products)


@wishlist_product_router.post(
    "/wishlist/{id}/products", response_model=WishlistProductsDataModel
)
async def create_wishlist_product(
    id: UUID4, product: WishlistProductsDataCreateModel  # noqa: A002
):
    """API for adding existing product to a existing wishlist."""
    wishlist = await Wishlist.get_or_404(id)
    return await wishlist.add_product(**product.data.validated_attributes)


@wishlist_product_router.put(
    "/wishlist/{id}/products/{pw_id}", response_model=WishlistProductsDataModel
)
async def update_wishlist_product(
    id: UUID4, pw_id: UUID4, pwm: WishlistProductsDataUpdateModel  # noqa: A002
):
    """API for updating product associated to a wishlist."""
    await Wishlist.get_or_404(id)
    wishlist_product = await WishlistProducts.get_or_404(pw_id)
    await wishlist_product.update(**pwm.data.non_null_attributes).apply()
    return wishlist_product


@wishlist_product_router.delete(
    "/wishlist/{id}/products/{pw_id}",
    response_class=Response,
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_wishlist_product(id: UUID4, pw_id: UUID4):  # noqa: A002
    """API for removing product from wishlist."""
    await Wishlist.get_or_404(id)
    wishlist_product = await WishlistProducts.get_or_404(pw_id)
    await wishlist_product.delete()
