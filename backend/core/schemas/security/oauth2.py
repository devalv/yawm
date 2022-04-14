# -*- coding: utf-8 -*-
"""Pydantic oauth2 models."""

from datetime import datetime
from typing import Any, Dict, Type, TypeVar, Union

from jose import jwt
from pydantic import UUID4, BaseModel, confloat, validator

from core import cached_settings

T = TypeVar("T", bound="TokenData")


class TokenData(BaseModel):
    sub: UUID4 | None = None
    username: str | None = None
    exp: Union[Type[float], datetime] = confloat(gt=datetime.utcnow().timestamp())

    @classmethod
    def decode(cls, token: str) -> T:
        decoded_token: Dict[str, Any] = jwt.decode(
            token, str(cached_settings.SECRET_KEY), algorithms=[cached_settings.ALGORITHM]
        )
        return cls(**decoded_token)


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    alg: str
    typ: str

    @validator("typ")
    def typ_check(cls, value):
        assert value == "JWT"
        return value

    @validator("alg")
    def alg_check(cls, value):
        assert value == cached_settings.ALGORITHM
        return value

    @validator("token_type")
    def token_type_check(cls, value):
        assert value.lower() == "bearer"
        return value
