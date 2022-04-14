"""Pydantic User models."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, SecretStr

from core.utils import BaseViewModel


class UserCreateModel(BaseModel):
    """Base User model."""

    username: str
    password: SecretStr = Field(min_length=8, max_length=254)


class UserViewModel(UserCreateModel, BaseViewModel):
    """User database row attributes model."""

    disabled: bool
    superuser: bool
    created_at: datetime
    password: str
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True
