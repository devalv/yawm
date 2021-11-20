# -*- coding: utf-8 -*-
"""Pydantic wishlist models."""

from pydantic import BaseModel

from core.utils import BaseUpdateModel, BaseViewModel


class WishlistCreateModel(BaseModel):
    name: str


class WishlistViewModel(WishlistCreateModel, BaseViewModel):
    username: str

    class Config:
        orm_mode = True


class WishlistUpdateModel(WishlistCreateModel, BaseUpdateModel):
    pass
