# -*- coding: utf-8 -*-
"""Wishlist rest-api handlers."""

from fastapi import APIRouter, Depends, Response, status
from fastapi_pagination.ext.gino import paginate
from fastapi_versioning import version

from core.database import UserGinoModel, WishlistGinoModel
from core.schemas import (
    WishlistDataCreateModel,
    WishlistDataModel,
    WishlistDataUpdateModel,
    WishlistModel,
)
from core.services.security import get_current_user, get_user_wishlist, get_wishlist
from core.utils import JsonApiPage

wishlist_router = APIRouter(redirect_slashes=True, tags=["wishlist"])


@wishlist_router.get("/wishlist", response_model=JsonApiPage[WishlistModel])
@version(1)
async def list_wishlist():
    """API for listing all the wishlists."""
    return await paginate(WishlistGinoModel.query)


@wishlist_router.get("/wishlist/{id}", response_model=WishlistDataModel)
@version(1)
async def get_wishlist(
    wishlist: WishlistGinoModel = Depends(get_wishlist)  # noqa: B008
):
    """API for getting a wishlist."""
    return wishlist


@wishlist_router.post("/wishlist", response_model=WishlistDataModel)
@version(1)
async def create_wishlist(
    wishlist: WishlistDataCreateModel,
    current_user: UserGinoModel = Depends(get_current_user),  # noqa: B008
):
    """API for creating a new wishlist."""
    return await WishlistGinoModel.create(
        user_id=current_user.id, **wishlist.data.validated_attributes
    )


@wishlist_router.put("/wishlist/{id}", response_model=WishlistDataModel)
@version(1)
async def update_wishlist(
    wishlist_updates: WishlistDataUpdateModel,
    wishlist: WishlistGinoModel = Depends(get_user_wishlist),  # noqa: B008
):
    """API for updating a wishlist."""
    await wishlist.update(**wishlist_updates.data.non_null_attributes).apply()
    return wishlist


@wishlist_router.delete(
    "/wishlist/{id}", response_class=Response, status_code=status.HTTP_204_NO_CONTENT
)
@version(1)
async def delete_wishlist(
    wishlist: WishlistGinoModel = Depends(get_user_wishlist)  # noqa: B008
):
    """API for deleting a wishlist."""
    await wishlist.delete()
