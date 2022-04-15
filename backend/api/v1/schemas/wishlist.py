# -*- coding: utf-8 -*-
"""Pydantic wishlist models."""

from core.utils import BaseUpdateModel, BaseViewModel


class WishlistUpdateModel(BaseUpdateModel):
    name: str


class WishlistViewModel(WishlistUpdateModel, BaseViewModel):
    name: str
    username: str

    class Config:
        orm_mode = True
