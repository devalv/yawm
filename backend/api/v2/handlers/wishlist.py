# -*- coding: utf-8 -*-
"""Wishlist rest-api handlers."""

from fastapi import APIRouter, Depends, status

from api.v2.schemas import WishlistProductsV2Model, WishlistViewV2Model
from core.database import UserGinoModel, WishlistGinoModel
from core.services.security import (
    get_current_active_user_by_access_token,
    get_user_wishlist_gino_obj,
    get_wishlist_gino_obj,
)

basename = "wishlists"
wishlist_router = APIRouter(redirect_slashes=True, tags=[basename])


@wishlist_router.post(f"/{basename}", response_model=WishlistViewV2Model)
async def create_wishlist(
    products: WishlistProductsV2Model,
    current_user: UserGinoModel = Depends(get_current_active_user_by_access_token),
):
    """API for creating a new wishlist."""
    # TODO: @devalv create products property for wishlist and use it like
    #  a product or user loader and use Orm mode

    wishlist_obj = await WishlistGinoModel.create_v2(
        user_id=current_user.id, product_urls=products.product_urls
    )

    wishlist_dict = wishlist_obj.to_dict()
    wishlist_dict["products"] = await wishlist_obj.get_products_v2()
    wishlist_dict["username"] = current_user.username
    return wishlist_dict


@wishlist_router.get(f"/{basename}/" + "{id}", response_model=WishlistViewV2Model)
async def get_wishlist(
    wishlist: WishlistGinoModel = Depends(get_wishlist_gino_obj),
):
    """API for getting a wishlist."""
    wishlist_dict = wishlist.to_dict()
    wishlist_dict["products"] = await wishlist.get_products_v2()
    wishlist_dict["username"] = wishlist.username
    return wishlist_dict


@wishlist_router.put(
    f"/{basename}/" + "{id}" + "/products-add",
    response_model=WishlistViewV2Model,
    status_code=status.HTTP_201_CREATED,
)
async def add_wishlist_products(
    products: WishlistProductsV2Model,
    wishlist_obj: WishlistGinoModel = Depends(get_user_wishlist_gino_obj),
    current_user: UserGinoModel = Depends(get_current_active_user_by_access_token),
):
    """API for adding products to a wishlist that already exists."""
    await wishlist_obj.add_products_v2(
        user_id=current_user.id, product_urls=products.product_urls
    )
    wishlist_dict = wishlist_obj.to_dict()
    wishlist_dict["products"] = await wishlist_obj.get_products_v2()
    wishlist_dict["username"] = current_user.username
    return wishlist_dict
