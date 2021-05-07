# -*- coding: utf-8 -*-
"""Wishlist rest-api handlers."""

import uuid

from fastapi import APIRouter, Response

from fastapi_pagination.ext.gino import paginate


from core.database.models.wishlist import Wishlist  # noqa: I100
from core.schemas.wishlist import WishlistModel, WishlistModelList  # noqa: I100
from core.utils import JsonApiPage  # noqa: I100

wishlist_router = APIRouter(prefix="/api/v1", redirect_slashes=True, tags=["wishlist"])


@wishlist_router.get("/wishlists", response_model=JsonApiPage[WishlistModelList])
async def list_wishlist():  # noqa: B008
    """API for listing all the wishlists."""
    wishlists = Wishlist.query
    return await paginate(wishlists)


@wishlist_router.post("/wishlists", response_model=WishlistModel)
async def add_wishlist(wishlist: WishlistModel):
    """API for creating a new wishlist."""
    rv = await Wishlist.create(name=wishlist.name)
    return rv.to_dict()


@wishlist_router.get("/wishlists/{uid}", response_model=WishlistModel)
async def get_wishlist(uid: uuid.UUID):
    """API for getting a wishlist."""
    wishlist = await Wishlist.get_or_404(uid)
    return wishlist.to_dict()


@wishlist_router.delete("/wishlists/{uid}", response_class=Response, status_code=204)
async def delete_wishlist(uid: uuid.UUID):
    """API for deleting a wishlist."""
    wishlist = await Wishlist.get_or_404(uid)
    await wishlist.delete()


@wishlist_router.put("/wishlists/{uid}", response_model=WishlistModel)
async def update_wishlist(uid: uuid.UUID, wishlist: WishlistModel):
    """API for updating a wishlist."""
    wishlist_obj = await Wishlist.get_or_404(uid)
    # remove empty field
    wishlist_dict = {k: v for k, v in wishlist.dict().items() if v is not None}

    await wishlist_obj.update(**wishlist_dict).apply()
    return wishlist_obj.to_dict()
