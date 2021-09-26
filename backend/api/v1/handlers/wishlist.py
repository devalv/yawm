# -*- coding: utf-8 -*-
"""Wishlist rest-api handlers."""

from fastapi import APIRouter, Depends, Response, status
from fastapi_pagination.ext.gino import paginate
from fastapi_pagination.links import Page

from core.database import UserGinoModel, WishlistGinoModel
from core.schemas import WishlistCreateModel, WishlistUpdateModel, WishlistViewModel
from core.services.security import (
    get_current_user_gino_obj,
    get_user_wishlist_gino_obj,
    get_wishlist_gino_obj,
)

wishlist_router = APIRouter(redirect_slashes=True, tags=["wishlist"])


@wishlist_router.get("/wishlist", response_model=Page[WishlistViewModel])
async def list_wishlist():
    """API for listing all the wishlists."""
    return await paginate(WishlistGinoModel.paginator_query())


@wishlist_router.get("/wishlist/{id}", response_model=WishlistViewModel)
async def get_wishlist(
    wishlist: WishlistGinoModel = Depends(get_wishlist_gino_obj),  # noqa: B008
):
    """API for getting a wishlist."""
    return wishlist


@wishlist_router.post("/wishlist", response_model=WishlistViewModel)
async def create_wishlist(
    wishlist: WishlistCreateModel,
    current_user: UserGinoModel = Depends(get_current_user_gino_obj),  # noqa: B008
):
    """API for creating a new wishlist."""
    wishlist_obj = await WishlistGinoModel.create(
        user_id=current_user.id, **wishlist.dict()
    )
    return await WishlistGinoModel.view_query(wishlist_obj.id)


@wishlist_router.put("/wishlist/{id}", response_model=WishlistViewModel)
async def update_wishlist(
    wishlist_updates: WishlistUpdateModel,
    wishlist: WishlistGinoModel = Depends(get_user_wishlist_gino_obj),  # noqa: B008
):
    """API for updating a wishlist."""
    await wishlist.update(**wishlist_updates.non_null_dict).apply()
    return await WishlistGinoModel.view_query(wishlist.id)


@wishlist_router.delete(
    "/wishlist/{id}", response_class=Response, status_code=status.HTTP_204_NO_CONTENT
)
async def delete_wishlist(
    wishlist: WishlistGinoModel = Depends(get_user_wishlist_gino_obj),  # noqa: B008
):
    """API for deleting a wishlist."""
    await wishlist.delete()
