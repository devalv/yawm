# -*- coding: utf-8 -*-
"""Pydantic wishlist-products models (v2)."""
from typing import Optional

from pydantic import UUID4, BaseModel


class WishlistProductV2Model(BaseModel):
    id: UUID4
    reserved: bool
    substitutable: bool

    class Config:
        orm_mode = True


class WishlistProductUpdateV2Model(BaseModel):
    reserved: Optional[bool] = None
    substitutable: Optional[bool] = None
