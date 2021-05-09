# -*- coding: utf-8 -*-
"""Project extra utils."""

from .fastapi_pagination import JsonApiPage
from .gino_models import JsonApiGinoModel
from .pydantic_models import (
    JsonApiDataPydanticCreateBaseModel,
    JsonApiDataPydanticModel,
    JsonApiDataPydanticUpdateBaseModel,
    JsonApiPydanticCreateBaseModel,
    JsonApiPydanticModel,
    JsonApiPydanticUpdateBaseModel,
)

__all__ = [
    "JsonApiPage",
    "JsonApiGinoModel",
    "JsonApiPydanticModel",
    "JsonApiDataPydanticCreateBaseModel",
    "JsonApiDataPydanticUpdateBaseModel",
    "JsonApiDataPydanticModel",
    "JsonApiPydanticCreateBaseModel",
    "JsonApiPydanticUpdateBaseModel",
]
