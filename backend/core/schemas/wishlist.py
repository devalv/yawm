# -*- coding: utf-8 -*-
"""Pydantic wishlist models."""

from pydantic import BaseModel

from core.utils import (  # noqa: I100
    JsonApiDataPydanticCreateBaseModel,
    JsonApiDataPydanticModel,
    JsonApiDataPydanticUpdateBaseModel,
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


class WishlistDataModel(JsonApiDataPydanticModel):
    """Wishlist data model."""

    data: WishlistModel


class WishlistCreateModel(JsonApiPydanticCreateBaseModel):
    """Wishlist creation serializer."""

    type: str = "wishlist"  # noqa: A003, VNE003
    attributes: WishlistAttributesModel


class WishlistDataCreateModel(JsonApiDataPydanticCreateBaseModel):
    """Wishlist data creation serializer."""

    data: WishlistCreateModel


class WishlistUpdateModel(JsonApiPydanticUpdateBaseModel):
    """Wishlist update serializer."""

    type: str = "wishlist"  # noqa: A003, VNE003
    attributes: WishlistUpdateAttributesModel


class WishlistDataUpdateModel(JsonApiDataPydanticUpdateBaseModel):
    """Wishlist data update serializer."""

    data: WishlistUpdateModel
