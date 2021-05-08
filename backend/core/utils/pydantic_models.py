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


class JsonApiPydanticListModel(JsonApiPydanticCreateBaseModel):
    """Pydantic pagination model."""

    id: uuid.UUID  # noqa: A002, A003, VNE003
