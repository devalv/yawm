# -*- coding: utf-8 -*-
"""Pydantic wishlist models."""

from pydantic import BaseModel

from core.utils import (  # noqa: I100
    JsonApiCreateBaseModel,
    JsonApiDBModel,
    JsonApiDataCreateBaseModel,
    JsonApiDataDBModel,
    JsonApiDataUpdateBaseModel,
    JsonApiUpdateBaseModel,
)


class WishlistAttributesModel(BaseModel):
    """Wishlist attributes serializer."""

    name: str


class WishlistUpdateAttributesModel(BaseModel):
    """Wishlist update attributes serializer."""

    name: str


class WishlistModel(JsonApiDBModel):
    """Wishlist serializer."""

    attributes: WishlistAttributesModel


class WishlistDataModel(JsonApiDataDBModel):
    """Wishlist data model."""

    data: WishlistModel


class WishlistCreateModel(JsonApiCreateBaseModel):
    """Wishlist creation serializer."""

    type: str = "wishlist"  # noqa: A003, VNE003
    attributes: WishlistAttributesModel


class WishlistDataCreateModel(JsonApiDataCreateBaseModel):
    """Wishlist data creation serializer."""

    data: WishlistCreateModel


class WishlistUpdateModel(JsonApiUpdateBaseModel):
    """Wishlist update serializer."""

    type: str = "wishlist"  # noqa: A003, VNE003
    attributes: WishlistUpdateAttributesModel


class WishlistDataUpdateModel(JsonApiDataUpdateBaseModel):
    """Wishlist data update serializer."""

    data: WishlistUpdateModel
