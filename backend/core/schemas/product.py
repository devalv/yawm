# -*- coding: utf-8 -*-
"""Pydantic product models."""

from typing import Optional

from pydantic import BaseModel, HttpUrl

from core.utils import (  # noqa: I100
    JsonApiPydanticCreateBaseModel,
    JsonApiPydanticModel,
)


class ProductAttributesModel(BaseModel):
    """Product attributes serializer."""

    name: str
    url: HttpUrl


class ProductUpdateAttributesModel(BaseModel):
    """Product update attributes serializer."""

    name: Optional[str]
    url: Optional[HttpUrl]
    name2: Optional[str]


class ProductModel(JsonApiPydanticModel):
    """Product list serializer."""

    attributes: ProductAttributesModel


class ProductCreateModel(JsonApiPydanticCreateBaseModel):
    """Product creation serializer."""

    type: str = "product"  # noqa: A003, VNE003
    attributes: ProductAttributesModel


class ProductUpdateModel(JsonApiPydanticCreateBaseModel):
    """Product update serializer."""

    type: str = "product"  # noqa: A003, VNE003
    attributes: ProductUpdateAttributesModel
