# -*- coding: utf-8 -*-
"""Pydantic models extra utils.

The main idea is to have a standard format for model interfaces.
"""

from datetime import datetime

from pydantic import UUID4, BaseModel


class BaseViewModel(BaseModel):
    """Abstract pydantic view model."""

    id: UUID4
    created_at: datetime
    updated_at: datetime | None = None


class BaseUpdateModel(BaseModel):
    """Abstract pydantic update model."""

    @property
    def non_null_dict(self):
        """Return non-null only attributes values."""
        result = dict()
        for attr, attr_value in self.__dict__.items():
            if attr_value is not None:
                result[attr] = attr_value
        return result
