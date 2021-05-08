# -*- coding: utf-8 -*-
"""Pydantic wishlist models."""

from pydantic import BaseModel

from core.utils import (  # noqa: I100
    JsonApiPydanticCreateBaseModel,
    JsonApiPydanticModel,
    JsonApiPydanticUpdateBaseModel,
)


class WishlistAttributesModel(BaseModel):
    """Wishlist attributes serializer."""

    name: str


class WishlistUpdateAttributesModel(BaseModel):
    """Wishlist update attributes serializer."""

    name: str


class WishlistModel(JsonApiPydanticModel):
    """Wishlist serializer."""

    attributes: WishlistAttributesModel


class WishlistCreateModel(JsonApiPydanticCreateBaseModel):
    """Wishlist creation serializer."""

    type: str = "wishlist"  # noqa: A003, VNE003
    attributes: WishlistAttributesModel


class WishlistUpdateModel(JsonApiPydanticUpdateBaseModel):
    """Wishlist update serializer."""

    type: str = "wishlist"  # noqa: A003, VNE003
    attributes: WishlistUpdateAttributesModel
