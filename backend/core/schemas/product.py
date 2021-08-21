# -*- coding: utf-8 -*-
"""Pydantic product models."""

from typing import Optional

from pydantic import BaseModel, HttpUrl

from core.utils import (
    JsonApiAttributesBaseModel,
    JsonApiCreateBaseModel,
    JsonApiDataCreateBaseModel,
    JsonApiDataDBModel,
    JsonApiDataUpdateBaseModel,
    JsonApiDBModel,
    JsonApiUpdateBaseModel,
)


class ProductAttributesModel(BaseModel):
    """Product attributes serializer."""

    name: str
    url: HttpUrl


class ProductViewAttributesModel(ProductAttributesModel, JsonApiAttributesBaseModel):
    pass


class ProductUpdateAttributesModel(BaseModel):
    """Product update attributes serializer."""

    name: Optional[str]
    url: Optional[HttpUrl]


class ProductModel(JsonApiDBModel):
    """Product serializer."""

    attributes: ProductViewAttributesModel


class ProductDataModel(JsonApiDataDBModel):
    """Product data model."""

    data: ProductModel


class ProductCreateModel(JsonApiCreateBaseModel):
    """Product creation serializer."""

    type: str = "product"  # noqa: A003, VNE003
    attributes: ProductAttributesModel


class ProductDataCreateModel(JsonApiDataCreateBaseModel):
    """Product data creation serializer."""

    data: ProductCreateModel


class ProductUpdateModel(JsonApiUpdateBaseModel):
    """Product update serializer."""

    type: str = "product"  # noqa: A003, VNE003
    attributes: ProductUpdateAttributesModel


class ProductDataUpdateModel(JsonApiDataUpdateBaseModel):
    """Project data update serializer."""

    data: ProductUpdateModel
