# -*- coding: utf-8 -*-
"""Wishlist rest-api handlers."""

import uuid

from fastapi import APIRouter, Response

from fastapi_pagination import Page
from fastapi_pagination.ext.gino import paginate

from core.database.models.wishlist import ProductWishlist, Wishlist  # noqa: I100
from core.schemas.wishlist import (
    AddProductWishlistModelList,
    ProductWishlistModel,
    ProductWishlistModelList,
    ProductWishlistUpdateModel,
)

wishlist_product_router = APIRouter(
    prefix="/api/v1", redirect_slashes=True, tags=["wishlist-product"]
)


@wishlist_product_router.get(
    "/wishlists/{uid}/products", response_model=Page[ProductWishlistModelList]
)
async def list_wishlist_products(uid: uuid.UUID):
    """API for getting all related products."""
    wishlist = await Wishlist.get_or_404(uid)
    return await paginate(wishlist.products_query)


@wishlist_product_router.post(
    "/wishlists/{uid}/products", response_model=ProductWishlistModel
)
async def add_wishlist_product(
    uid: uuid.UUID, product_wishlist: AddProductWishlistModelList
):
    """API for adding existing product to a existing wishlist."""
    # TODO: add many products
    wishlist = await Wishlist.get_or_404(uid)
    rv = await wishlist.add_product(product_wishlist.product_uid)
    return rv.to_dict()


@wishlist_product_router.put(
    "/wishlists/{uid}/products/{pw_uid}/reserve", response_model=ProductWishlistModel
)
async def reserve_wishlist_product(
    uid: uuid.UUID, pw_uid: uuid.UUID, pwm: ProductWishlistUpdateModel
):
    """API for reserving existing product-wishlist record."""
    # TODO: check wishlist owner
    product_wishlist = await ProductWishlist.get_or_404(pw_uid)
    await product_wishlist.update(reserved=pwm.reserved).apply()
    return product_wishlist.to_dict()


@wishlist_product_router.put(
    "/wishlists/{uid}/products/{pw_uid}/substitute", response_model=ProductWishlistModel
)
async def substitute_wishlist_product(
    uid: uuid.UUID, pw_uid: uuid.UUID, pwm: ProductWishlistUpdateModel
):
    """API for set Product.substitutable existing product-wishlist record."""
    # TODO: check wishlist owner
    product_wishlist = await ProductWishlist.get_or_404(pw_uid)
    await product_wishlist.update(substitutable=pwm.substitutable).apply()
    return product_wishlist.to_dict()


@wishlist_product_router.delete(
    "/wishlists/{uid}/products/{pw_uid}", response_class=Response, status_code=204
)
async def delete_wishlist_product(uid: uuid.UUID, pw_uid: uuid.UUID):
    """API for removing product from wishlist."""
    product_wishlist = await ProductWishlist.get_or_404(pw_uid)
    await product_wishlist.delete()
