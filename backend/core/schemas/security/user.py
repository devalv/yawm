"""Pydantic User models."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from core.utils import BaseViewModel


class UserCreateModel(BaseModel):
    """Base User model."""

    username: str
    password: str = Field(min_length=8, max_length=254)


class UserViewModel(BaseViewModel):
    """User database row attributes model."""

    username: str
    disabled: bool
    superuser: bool
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True
