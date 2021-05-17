# -*- coding: utf-8 -*-
"""Pydantic models extra utils.

The main idea is to have a standard format for model interfaces.
"""

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


class JsonApiDataPydanticCreateBaseModel(BaseModel):
    """Pydantic JSON:API data creation model."""

    data: JsonApiPydanticCreateBaseModel


class JsonApiPydanticUpdateBaseModel(JsonApiPydanticCreateBaseModel):
    """Pydantic update model."""


class JsonApiDataPydanticUpdateBaseModel(JsonApiDataPydanticCreateBaseModel):
    """Pydantic JSON:API data update model."""


class JsonApiPydanticModel(JsonApiPydanticCreateBaseModel):
    """Pydantic object model.

    It`s a proper response_model for JsonApiPage,
    for other response_models use JsonApiDataPydanticModel instead.
    """

    id: uuid.UUID  # noqa: A002, A003, VNE003

    class Config:  # noqa: D106
        orm_mode = True


class JsonApiDataPydanticModel(BaseModel):
    """JSON:API says that `data` key must be on a response."""

    data: JsonApiPydanticModel

    class Config:  # noqa: D106
        orm_mode = True