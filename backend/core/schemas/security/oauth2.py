# -*- coding: utf-8 -*-
"""Pydantic oauth2 models."""

from pydantic import BaseModel


class Token(BaseModel):  # noqa: D101
    access_token: str
    token_type: str


class TokenData(BaseModel):  # noqa: D101
    username: str = None
    email: str = None
