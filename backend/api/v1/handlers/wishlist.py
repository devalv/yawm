# -*- coding: utf-8 -*-
"""Wishlist rest-api handlers."""

from fastapi import APIRouter, Response, status

from fastapi_pagination.ext.gino import paginate

from pydantic import UUID4

from core.database.models.wishlist import Wishlist
from core.schemas import (
    WishlistDataCreateModel,
    WishlistDataModel,
    WishlistDataUpdateModel,
    WishlistModel,
)
from core.utils import JsonApiPage

wishlist_router = APIRouter(prefix="/api/v1", redirect_slashes=True, tags=["wishlist"])


@wishlist_router.get("/wishlist", response_model=JsonApiPage[WishlistModel])
async def list_wishlist():
    """API for listing all the wishlists."""
    return await paginate(Wishlist.query)


@wishlist_router.get("/wishlist/{id}", response_model=WishlistDataModel)
async def get_wishlist(id: UUID4):  # noqa: A002
    """API for getting a wishlist."""
    return await Wishlist.get_or_404(id)


@wishlist_router.post("/wishlist", response_model=WishlistDataModel)
async def create_wishlist(wishlist: WishlistDataCreateModel):
    """API for creating a new wishlist."""
    return await Wishlist.create(**wishlist.data.validated_attributes)


@wishlist_router.put("/wishlist/{id}", response_model=WishlistDataModel)
async def update_wishlist(id: UUID4, wishlist: WishlistDataUpdateModel):  # noqa: A002
    """API for updating a wishlist."""
    wishlist_obj = await Wishlist.get_or_404(id)
    await wishlist_obj.update(**wishlist.data.non_null_attributes).apply()
    return wishlist_obj


@wishlist_router.delete(
    "/wishlist/{id}", response_class=Response, status_code=status.HTTP_204_NO_CONTENT
)
async def delete_wishlist(id: UUID4):  # noqa: A002
    """API for deleting a wishlist."""
    wishlist = await Wishlist.get_or_404(id)
    await wishlist.delete()
