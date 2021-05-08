# -*- coding: utf-8 -*-
"""Pydantic models extra utils."""

import uuid
from abc import abstractmethod

from pydantic import BaseModel


class JsonApiPydanticAttributesBaseModel(BaseModel):
    """Abstract attributes pydantic model."""

    @abstractmethod
    def __init__(self):
        """Main model should be redefined."""


class JsonApiPydanticCreateBaseModel(BaseModel):
    """Pydantic BaseModel extra utilities."""

    type: str  # noqa: A002, A003, VNE003
    attributes: JsonApiPydanticAttributesBaseModel

    @property
    def validated_attributes(self):
        """Validated model attributes."""
        result = dict()

        for attr, attr_value in self.attributes:
            result[attr] = attr_value

        return result

    @property
    def non_null_attributes(self):
        """Return non-null only attributes values."""
        result = dict()

        for attr, attr_value in self.attributes:
            if attr_value is not None:
                result[attr] = attr_value

        return result

    class Config:  # noqa: D106
        orm_mode = True


class JsonApiPydanticModel(JsonApiPydanticCreateBaseModel):
    """Pydantic pagination model."""

    id: uuid.UUID  # noqa: A002, A003, VNE003
