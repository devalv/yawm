# -*- coding: utf-8 -*-
"""Pydantic wishlist models."""

from pydantic import BaseModel

from core.utils import BaseUpdateModel, BaseViewModel


class WishlistCreateModel(BaseModel):
    name: str


class WishlistViewModel(WishlistCreateModel, BaseViewModel):
    class Config:
        orm_mode = True


class WishlistUpdateModel(WishlistCreateModel, BaseUpdateModel):
    pass


# class YobaModel(BaseModel):
#     TODO: @devalv ref
# id: UUID4
# name: str
# updated_at: Optional[datetime]
# created_at: datetime
# username: str

# class Config:  # noqa: D106
#     orm_mode = True
