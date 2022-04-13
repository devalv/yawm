# -*- coding: utf-8 -*-
"""Pydantic User models."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from core.utils import BaseViewModel


class UserCreateModel(BaseModel):
    """Base User model."""

    username: str


class UserViewModel(UserCreateModel, BaseViewModel):
    """User database row attributes model."""

    disabled: bool
    superuser: bool
    created_at: datetime
    password: str
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True
