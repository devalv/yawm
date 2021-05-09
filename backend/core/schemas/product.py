# -*- coding: utf-8 -*-
"""Pydantic product models."""

from typing import Optional

from pydantic import BaseModel, HttpUrl

from core.utils import (  # noqa: I100
    JsonApiDataPydanticCreateBaseModel,
    JsonApiDataPydanticModel,
    JsonApiDataPydanticUpdateBaseModel,
    JsonApiPydanticCreateBaseModel,
    JsonApiPydanticModel,
    JsonApiPydanticUpdateBaseModel,
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
    """Product serializer."""

    attributes: ProductAttributesModel


class ProductDataModel(JsonApiDataPydanticModel):
    """Product data model."""

    data: ProductModel


class ProductCreateModel(JsonApiPydanticCreateBaseModel):
    """Product creation serializer."""

    type: str = "product"  # noqa: A003, VNE003
    attributes: ProductAttributesModel


class ProductDataCreateModel(JsonApiDataPydanticCreateBaseModel):
    """Product data creation serializer."""

    data: ProductCreateModel


class ProductUpdateModel(JsonApiPydanticUpdateBaseModel):
    """Product update serializer."""

    type: str = "product"  # noqa: A003, VNE003
    attributes: ProductUpdateAttributesModel


class ProductDataUpdateModel(JsonApiDataPydanticUpdateBaseModel):
    """Project data update serializer."""

    data: ProductUpdateModel
