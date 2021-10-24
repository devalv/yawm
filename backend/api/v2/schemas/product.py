# -*- coding: utf-8 -*-
"""Pydantic product models (v2)."""

from pydantic import BaseModel, HttpUrl

from core.utils import BaseViewModel


class ProductCreateV2Model(BaseModel):
    url: HttpUrl


class ProductViewV2Model(BaseViewModel):
    name: str
    url: HttpUrl
    reserved: bool
    substitutable: bool

    class Config:
        orm_mode = True
