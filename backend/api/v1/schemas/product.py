# -*- coding: utf-8 -*-
"""Pydantic product models."""
from pydantic import BaseModel, HttpUrl

from core.utils import BaseUpdateModel, BaseViewModel


class ProductCreateModel(BaseModel):
    name: str
    url: HttpUrl


class ProductViewModel(ProductCreateModel, BaseViewModel):
    username: str

    class Config:
        orm_mode = True


class ProductUpdateModel(BaseUpdateModel):
    name: str | None
    url: HttpUrl | None
