# -*- coding: utf-8 -*-
"""Pydantic User models."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, UUID4


class BaseUserModel(BaseModel):
    """Base User model."""

    ext_id: Optional[str] = None
    disabled = Optional[bool] = False
    superuser = Optional[bool] = False
    created = Optional[datetime] = None
    username = Optional[str] = None
    given_name = Optional[str] = None
    family_name = Optional[str] = None
    full_name = Optional[str] = None


# TODO: JSON:API schemas?
# TODO: create user model
# TODO: update user model


class BaseUserDB(BaseModel):
    """Database row model."""

    id: UUID4  # noqa: A003, VNE003
    ext_id: str
    disabled = bool
    superuser = bool
    created = datetime
    username = str
    given_name = str
    family_name = str
    full_name = str

    class Config:  # noqa: D106
        orm_mode = True
