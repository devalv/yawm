# -*- coding: utf-8 -*-
"""Wishlist rest-api handlers."""

from api.v2.schemas import WishlistCreateV2Model, WishlistViewV2Model
from fastapi import APIRouter, Depends

from core.database import UserGinoModel, WishlistGinoModel
from core.services.security import get_current_user_gino_obj, get_wishlist_gino_obj

basename = "wishlists"
wishlist_router = APIRouter(redirect_slashes=True, tags=[basename])


@wishlist_router.post(f"/{basename}", response_model=WishlistViewV2Model)
async def create_wishlist(
    wishlist: WishlistCreateV2Model,
    current_user: UserGinoModel = Depends(get_current_user_gino_obj),  # noqa: B008
):
    """API for creating a new wishlist."""
    # TODO: @devalv create produycts property for wishlist and use it like
    #  a product or user loader and use Orm mode

    wishlist_obj = await WishlistGinoModel.create_v2(
        user_id=current_user.id, product_urls=wishlist.product_urls
    )

    wishlist_dict = wishlist_obj.to_dict()
    wishlist_dict["products"] = await wishlist_obj.get_products_v2()

    return wishlist_dict


@wishlist_router.get(f"/{basename}/" + "{id}", response_model=WishlistViewV2Model)
async def get_wishlist(
    wishlist: WishlistGinoModel = Depends(get_wishlist_gino_obj),  # noqa: B008
):
    """API for getting a wishlist."""
    wishlist_dict = wishlist.to_dict()
    wishlist_dict["products"] = await wishlist.get_products_v2()
    wishlist_dict["username"] = wishlist.username
    return wishlist_dict
