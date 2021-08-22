# -*- coding: utf-8 -*-
"""Wishlist rest-api handlers."""

from fastapi import APIRouter, Depends, Response, status
from fastapi_pagination.ext.gino import paginate
from fastapi_pagination.links import Page

from core.database import UserGinoModel, WishlistGinoModel
from core.schemas import WishlistCreateModel, WishlistUpdateModel, WishlistViewModel

# from core.schemas.wishlist import YobaModel  # noqa: E800
from core.services.security import get_current_user, get_user_wishlist, get_wishlist

wishlist_router = APIRouter(redirect_slashes=True, tags=["wishlist"])


@wishlist_router.get("/wishlist", response_model=Page[WishlistViewModel])
# @wishlist_router.get("/wishlist", response_model=JsonApiPage[WishlistModel])
async def list_wishlist():
    """API for listing all the wishlists."""
    return await paginate(WishlistGinoModel.query)
    # return await paginate(WishlistGinoModel.paginator_list())


@wishlist_router.get("/wishlist/{id}", response_model=WishlistViewModel)
async def get_wishlist(
    wishlist: WishlistGinoModel = Depends(get_wishlist),  # noqa: B008
):
    """API for getting a wishlist."""
    return wishlist


@wishlist_router.post("/wishlist", response_model=WishlistViewModel)
async def create_wishlist(
    wishlist: WishlistCreateModel,
    current_user: UserGinoModel = Depends(get_current_user),  # noqa: B008
):
    """API for creating a new wishlist."""
    return await WishlistGinoModel.create(user_id=current_user.id, **wishlist.dict())


@wishlist_router.put("/wishlist/{id}", response_model=WishlistViewModel)
async def update_wishlist(
    wishlist_updates: WishlistUpdateModel,
    wishlist: WishlistGinoModel = Depends(get_user_wishlist),  # noqa: B008
):
    """API for updating a wishlist."""
    await wishlist.update(**wishlist_updates.non_null_dict).apply()
    return wishlist


@wishlist_router.delete(
    "/wishlist/{id}", response_class=Response, status_code=status.HTTP_204_NO_CONTENT
)
async def delete_wishlist(
    wishlist: WishlistGinoModel = Depends(get_user_wishlist),  # noqa: B008
):
    """API for deleting a wishlist."""
    await wishlist.delete()
