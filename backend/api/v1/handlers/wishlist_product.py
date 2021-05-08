# -*- coding: utf-8 -*-
"""Wishlist rest-api handlers."""

import uuid

from fastapi import APIRouter, Response

from fastapi_pagination.ext.gino import paginate

from core.database.models.wishlist import ProductWishlist, Wishlist  # noqa: I100
from core.schemas.wishlist import (
    AddProductWishlistModel,
    ProductWishlistModel,
    ProductWishlistModelList,
    ProductWishlistUpdateModel,
)
from core.utils import JsonApiPage  # noqa: I100

wishlist_product_router = APIRouter(
    prefix="/api/v1", redirect_slashes=True, tags=["wishlist-product"]
)


@wishlist_product_router.get(
    "/wishlists/{id}/products", response_model=JsonApiPage[ProductWishlistModelList]
)
async def list_wishlist_products(id: uuid.UUID):  # noqa: A002
    """API for getting all related products."""
    wishlist = await Wishlist.get_or_404(id)
    return await paginate(wishlist.products)


@wishlist_product_router.post(
    "/wishlists/{id}/products", response_model=ProductWishlistModel
)
async def add_wishlist_product(
    id: uuid.UUID, product_wishlist: AddProductWishlistModel  # noqa: A002
):
    """API for adding existing product to a existing wishlist."""
    # TODO: add many products
    wishlist = await Wishlist.get_or_404(id)
    rv = await wishlist.add_product(product_wishlist.product_id)
    return rv.to_dict()


@wishlist_product_router.put(
    "/wishlists/{id}/products/{pw_id}/reserve", response_model=ProductWishlistModel
)
async def reserve_wishlist_product(
    id: uuid.UUID, pw_id: uuid.UUID, pwm: ProductWishlistUpdateModel  # noqa: A002
):
    """API for reserving existing product-wishlist record."""
    # TODO: check wishlist owner
    await Wishlist.get_or_404(id)
    product_wishlist = await ProductWishlist.get_or_404(pw_id)
    await product_wishlist.update(reserved=pwm.reserved).apply()
    return product_wishlist.to_dict()


@wishlist_product_router.put(
    "/wishlists/{id}/products/{pw_id}/substitute", response_model=ProductWishlistModel
)
async def substitute_wishlist_product(
    id: uuid.UUID, pw_id: uuid.UUID, pwm: ProductWishlistUpdateModel  # noqa: A002
):
    """API for set Product.substitutable existing product-wishlist record."""
    # TODO: check wishlist owner
    await Wishlist.get_or_404(id)
    product_wishlist = await ProductWishlist.get_or_404(pw_id)
    await product_wishlist.update(substitutable=pwm.substitutable).apply()
    return product_wishlist.to_dict()


@wishlist_product_router.delete(
    "/wishlists/{id}/products/{pw_id}", response_class=Response, status_code=204
)
async def delete_wishlist_product(id: uuid.UUID, pw_id: uuid.UUID):  # noqa: A002
    """API for removing product from wishlist."""
    # TODO: check wishlist owner
    await Wishlist.get_or_404(id)
    product_wishlist = await ProductWishlist.get_or_404(pw_id)
    await product_wishlist.delete()
