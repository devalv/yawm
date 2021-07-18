# -*- coding: utf-8 -*-
"""Pydantic utils models."""

from typing import Optional

from pydantic import BaseModel, HttpUrl

from core.utils.pydantic_models import (
    JsonApiCreateBaseModel,
    JsonApiDataCreateBaseModel,
)


class ExtractUrlAttributesInModel(BaseModel):
    """Extract url attributes serializer."""

    url: HttpUrl


class ExtractUrlAttributesOutModel(BaseModel):
    """Extract url attributes serializer."""

    h1: Optional[str]


class ExtractUrlInModel(JsonApiCreateBaseModel):
    """Extract url creation serializer."""

    type: str = "utils"  # noqa: A003, VNE003
    attributes: ExtractUrlAttributesInModel


class ExtractUrlOutModel(JsonApiCreateBaseModel):
    """Extract url response serializer."""

    type: str = "utils"  # noqa: A003, VNE003
    attributes: ExtractUrlAttributesOutModel


class ExtractUrlDataInModel(JsonApiDataCreateBaseModel):
    """Extract url data creation serializer."""

    data: ExtractUrlInModel


class ExtractUrlModelDataOutModel(BaseModel):
    """Extract url response data model."""

    data: ExtractUrlOutModel
