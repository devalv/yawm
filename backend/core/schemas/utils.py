# -*- coding: utf-8 -*-
"""Pydantic utils models."""

from typing import Optional

from pydantic import BaseModel, HttpUrl


class ExtractUrlInModel(BaseModel):
    """Extract url attributes serializer."""

    url: HttpUrl


class ExtractUrlOutModel(BaseModel):
    """Extract url attributes serializer."""

    h1: Optional[str]
