# -*- coding: utf-8 -*-
"""Pydantic product models."""
from typing import Optional

from pydantic import BaseModel, HttpUrl

from core.utils import BaseUpdateModel, BaseViewModel


class ProductCreateModel(BaseModel):
    name: str
    url: HttpUrl


class ProductViewModel(ProductCreateModel, BaseViewModel):
    class Config:
        orm_mode = True


class ProductUpdateModel(BaseUpdateModel):
    name: Optional[str]
    url: Optional[HttpUrl]
