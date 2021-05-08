# -*- coding: utf-8 -*-
"""Wishlist rest-api handlers."""

import uuid

from fastapi import APIRouter, Response

from fastapi_pagination.ext.gino import paginate

from core.database.models.wishlist import Wishlist, WishlistProducts  # noqa: I100
from core.schemas import (
    WishlistProductsCreateModel,
    WishlistProductsModel,
    WishlistProductsUpdateModel,
)
from core.utils import JsonApiPage  # noqa: I100

wishlist_product_router = APIRouter(
    prefix="/api/v1", redirect_slashes=True, tags=["wishlist-products"]
)


@wishlist_product_router.get(
    "/wishlist/{id}/products", response_model=JsonApiPage[WishlistProductsModel]
)
async def list_wishlist_products(id: uuid.UUID):  # noqa: A002
    """API for getting all related products."""
    wishlist = await Wishlist.get_or_404(id)
    return await paginate(wishlist.products)


@wishlist_product_router.post(
    "/wishlist/{id}/products", response_model=WishlistProductsModel
)
async def create_wishlist_product(
    id: uuid.UUID, product: WishlistProductsCreateModel  # noqa: A002
):
    """API for adding existing product to a existing wishlist."""
    # TODO: add many products
    wishlist = await Wishlist.get_or_404(id)
    return await wishlist.add_product(**product.validated_attributes)


@wishlist_product_router.put(
    "/wishlist/{id}/products/{pw_id}", response_model=WishlistProductsModel
)
async def update_wishlist_product(
    id: uuid.UUID, pw_id: uuid.UUID, pwm: WishlistProductsUpdateModel  # noqa: A002
):
    """API for updating product associated to a wishlist."""
    await Wishlist.get_or_404(id)
    wishlist_product = await WishlistProducts.get_or_404(pw_id)
    await wishlist_product.update(**pwm.non_null_attributes).apply()
    return wishlist_product


@wishlist_product_router.delete(
    "/wishlist/{id}/products/{pw_id}", response_class=Response, status_code=204
)
async def delete_wishlist_product(id: uuid.UUID, pw_id: uuid.UUID):  # noqa: A002
    """API for removing product from wishlist."""
    await Wishlist.get_or_404(id)
    wishlist_product = await WishlistProducts.get_or_404(pw_id)
    await wishlist_product.delete()
