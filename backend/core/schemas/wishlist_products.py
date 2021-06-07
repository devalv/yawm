# -*- coding: utf-8 -*-
"""Pydantic wishlist products models."""

from typing import Optional

from pydantic import BaseModel, UUID4

from core.utils import (  # noqa: I100
    JsonApiDataPydanticCreateBaseModel,
    JsonApiDataPydanticModel,
    JsonApiDataPydanticUpdateBaseModel,
    JsonApiPydanticCreateBaseModel,
    JsonApiPydanticModel,
    JsonApiPydanticUpdateBaseModel,
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


class WishlistProductsModel(JsonApiPydanticModel):
    """Wishlist products serializer."""

    attributes: WishlistProductsAttributesModel


class WishlistProductsDataModel(JsonApiDataPydanticModel):
    """Wishlist products data model."""

    data: WishlistProductsModel


class WishlistProductsCreateModel(JsonApiPydanticCreateBaseModel):
    """Wishlist products creation serializer."""

    type: str = "wishlist_products"  # noqa: A003, VNE003
    attributes: WishlistProductsCreateAttributesModel


class WishlistProductsDataCreateModel(JsonApiDataPydanticCreateBaseModel):
    """Wishlist products data creation serializer."""

    data: WishlistProductsCreateModel


class WishlistProductsUpdateModel(JsonApiPydanticUpdateBaseModel):
    """Wishlist products update serializer."""

    type: str = "wishlist_products"  # noqa: A003, VNE003
    attributes: WishlistProductsUpdateAttributesModel


class WishlistProductsDataUpdateModel(JsonApiDataPydanticUpdateBaseModel):
    """Wishlist products data update serializer."""

    data: WishlistProductsUpdateModel
