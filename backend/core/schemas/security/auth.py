# -*- coding: utf-8 -*-
"""Pydantic User models."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from core.utils import BaseViewModel


class BaseUserModel(BaseModel):
    """Base User model."""

    disabled: Optional[bool] = False
    superuser: Optional[bool] = False
    username: Optional[str] = None
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    full_name: Optional[str] = None


class UserCreateModel(BaseUserModel):
    """User attributes creation serializer."""

    ext_id: str
    username: str


class UserViewModel(BaseUserModel, BaseViewModel):
    """User database row attributes model."""

    ext_id: str
    disabled: bool
    superuser: bool
    created_at: datetime
    username: str
    updated_at: Optional[datetime]
    given_name: Optional[str]
    family_name: Optional[str]
    full_name: Optional[str]

    class Config:
        orm_mode = True
