# -*- coding: utf-8 -*-
"""Pydantic User models."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from core.utils import (  # noqa: I100
    JsonApiCreateBaseModel,
    JsonApiDBModel,
    JsonApiDataCreateBaseModel,
    JsonApiDataDBModel,
    JsonApiDataUpdateBaseModel,
    JsonApiUpdateBaseModel,
)


class BaseUserAttributesModel(BaseModel):
    """Base User model."""

    disabled: Optional[bool]
    superuser: Optional[bool]
    username: Optional[str]
    given_name: Optional[str]
    family_name: Optional[str]
    full_name: Optional[str]


class UserCreateAttributesModel(BaseUserAttributesModel):
    """User attributes creation serializer."""

    ext_id: str
    username: str


class UserCreateModel(JsonApiCreateBaseModel):
    """User creation serializer."""

    type: str = "user"  # noqa: A003, VNE003
    attributes = UserCreateAttributesModel


class UserDataCreateModel(JsonApiDataCreateBaseModel):
    """User data creation serializer."""

    data: UserCreateModel


class UserUpdateModel(BaseUserAttributesModel):
    """User attributes update serializer."""


class UserUpdateModel(JsonApiUpdateBaseModel):
    """User update serializer."""

    type: str = "user"  # noqa: A003, VNE003
    attributes = UserUpdateModel


class UserDataUpdateModel(JsonApiDataUpdateBaseModel):
    """User data update serializer."""

    data: UserUpdateModel


class BaseUserDB(BaseModel):
    """User database row attributes model."""

    ext_id: str
    disabled = bool
    superuser = bool
    created = datetime
    username = str
    given_name = str
    family_name = str
    full_name = str


class UserDBModel(JsonApiDBModel):
    """User serializer."""

    attributes: BaseUserDB


class UserDBDataModel(JsonApiDataDBModel):
    """User data model."""

    data: UserDBModel
