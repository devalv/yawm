# -*- coding: utf-8 -*-
"""Pydantic wishlist products models."""

from typing import Optional

from pydantic import BaseModel, UUID4

from core.utils import (
    JsonApiCreateBaseModel,
    JsonApiDBModel,
    JsonApiDataCreateBaseModel,
    JsonApiDataDBModel,
    JsonApiDataUpdateBaseModel,
    JsonApiUpdateBaseModel,
)


class WishlistProductsAttributesModel(BaseModel):
    """Wishlist products attributes serializer."""

    # TODO: JSON:API related?

    wishlist_id: UUID4
    product_id: UUID4
    reserved: bool
    substitutable: bool


class WishlistProductsCreateAttributesModel(BaseModel):
    """Wishlist products create attributes serializer."""

    # TODO: JSON:API related?

    product_id: UUID4
    reserved: bool
    substitutable: bool


class WishlistProductsUpdateAttributesModel(BaseModel):
    """Wishlist products update attributes serializer."""

    # TODO: JSON:API related?

    product_id: Optional[UUID4]
    reserved: Optional[bool]
    substitutable: Optional[bool]


class WishlistProductsModel(JsonApiDBModel):
    """Wishlist products serializer."""

    attributes: WishlistProductsAttributesModel


class WishlistProductsDataModel(JsonApiDataDBModel):
    """Wishlist products data model."""

    data: WishlistProductsModel


class WishlistProductsCreateModel(JsonApiCreateBaseModel):
    """Wishlist products creation serializer."""

    type: str = "wishlist_products"  # noqa: A003, VNE003
    attributes: WishlistProductsCreateAttributesModel


class WishlistProductsDataCreateModel(JsonApiDataCreateBaseModel):
    """Wishlist products data creation serializer."""

    data: WishlistProductsCreateModel


class WishlistProductsUpdateModel(JsonApiUpdateBaseModel):
    """Wishlist products update serializer."""

    type: str = "wishlist_products"  # noqa: A003, VNE003
    attributes: WishlistProductsUpdateAttributesModel


class WishlistProductsDataUpdateModel(JsonApiDataUpdateBaseModel):
    """Wishlist products data update serializer."""

    data: WishlistProductsUpdateModel
