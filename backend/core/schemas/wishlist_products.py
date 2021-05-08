# -*- coding: utf-8 -*-
"""Pydantic wishlist products models."""

import uuid
from typing import Optional

from pydantic import BaseModel

from core.utils import (  # noqa: I100
    JsonApiPydanticCreateBaseModel,
    JsonApiPydanticModel,
    JsonApiPydanticUpdateBaseModel,
)


class WishlistProductsAttributesModel(BaseModel):
    """Wishlist products attributes serializer."""

    wishlist_id: uuid.UUID  # TODO: JSON:API related?
    product_id: uuid.UUID  # TODO: JSON:API related?
    reserved: bool
    substitutable: bool


class WishlistProductsCreateAttributesModel(BaseModel):
    """Wishlist products create attributes serializer."""

    product_id: uuid.UUID  # TODO: JSON:API related?
    reserved: bool
    substitutable: bool


class WishlistProductsUpdateAttributesModel(BaseModel):
    """Wishlist products update attributes serializer."""

    product_id: Optional[uuid.UUID]  # TODO: JSON:API related?
    reserved: Optional[bool]
    substitutable: Optional[bool]


class WishlistProductsModel(JsonApiPydanticModel):
    """Wishlist products serializer."""

    attributes: WishlistProductsAttributesModel


class WishlistProductsCreateModel(JsonApiPydanticCreateBaseModel):
    """Wishlist products creation serializer."""

    type: str = "wishlist_products"  # noqa: A003, VNE003
    attributes: WishlistProductsCreateAttributesModel


class WishlistProductsUpdateModel(JsonApiPydanticUpdateBaseModel):
    """Wishlist products update serializer."""

    type: str = "wishlist_products"  # noqa: A003, VNE003
    attributes: WishlistProductsUpdateAttributesModel
