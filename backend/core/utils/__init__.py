# -*- coding: utf-8 -*-
"""Project extra utils."""

from .fastapi_pagination import JsonApiPage
from .gino_models import JsonApiGinoModel
from .pydantic_models import (
    JsonApiCreateBaseModel,
    JsonApiDBModel,
    JsonApiDataCreateBaseModel,
    JsonApiDataDBModel,
    JsonApiDataUpdateBaseModel,
    JsonApiUpdateBaseModel,
)

__all__ = [
    "JsonApiPage",
    "JsonApiGinoModel",
    "JsonApiDBModel",
    "JsonApiDataCreateBaseModel",
    "JsonApiDataUpdateBaseModel",
    "JsonApiDataDBModel",
    "JsonApiCreateBaseModel",
    "JsonApiUpdateBaseModel",
]
