# -*- coding: utf-8 -*-
"""Wishlist rest-api handlers."""

import uuid

from fastapi import APIRouter, Response

from fastapi_pagination.ext.gino import paginate


from core.database.models.wishlist import Wishlist  # noqa: I100
from core.schemas.wishlist import (
    WishlistCreateModel,
    WishlistModel,
    WishlistUpdateModel,
)
from core.utils import JsonApiPage  # noqa: I100

wishlist_router = APIRouter(prefix="/api/v1", redirect_slashes=True, tags=["wishlist"])


@wishlist_router.get("/wishlists", response_model=JsonApiPage[WishlistModel])
async def list_wishlist():
    """API for listing all the wishlists."""
    return await paginate(Wishlist.query)


@wishlist_router.get("/wishlists/{id}", response_model=WishlistModel)
async def get_wishlist(id: uuid.UUID):  # noqa: A002
    """API for getting a wishlist."""
    return await Wishlist.get_or_404(id)


@wishlist_router.post("/wishlists", response_model=WishlistModel)
async def create_wishlist(wishlist: WishlistCreateModel):
    """API for creating a new wishlist."""
    return await Wishlist.create(**wishlist.validated_attributes)


@wishlist_router.put("/wishlists/{id}", response_model=WishlistModel)
async def update_wishlist(id: uuid.UUID, wishlist: WishlistUpdateModel):  # noqa: A002
    """API for updating a wishlist."""
    wishlist_obj = await Wishlist.get_or_404(id)
    await wishlist_obj.update(**wishlist.non_null_attributes).apply()
    return wishlist_obj


@wishlist_router.delete("/wishlists/{id}", response_class=Response, status_code=204)
async def delete_wishlist(id: uuid.UUID):  # noqa: A002
    """API for deleting a wishlist."""
    wishlist = await Wishlist.get_or_404(id)
    await wishlist.delete()
