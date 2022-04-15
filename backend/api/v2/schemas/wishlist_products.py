# -*- coding: utf-8 -*-
"""Pydantic wishlist-products models (v2)."""
from datetime import datetime

from pydantic import UUID4, BaseModel


class WishlistProductV2Model(BaseModel):
    id: UUID4
    reserved: bool
    substitutable: bool
    created_at: datetime
    name: str

    class Config:
        orm_mode = True


class WishlistProductUpdateV2Model(BaseModel):
    reserved: bool | None
    substitutable: bool | None
    name: str | None
