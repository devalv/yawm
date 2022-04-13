# -*- coding: utf-8 -*-
"""Pydantic oauth2 models."""

from datetime import datetime
from typing import Type, Union

from jose import jwt
from pydantic import UUID4, BaseModel, SecretStr, confloat, validator

from core import cached_settings


class RefreshToken(BaseModel):
    id: UUID4
    username: str
    exp: Union[Type[float], datetime] = confloat(gt=datetime.utcnow().timestamp())

    @classmethod
    def decode(cls, token: str):
        return jwt.decode(
            token, str(cached_settings.SECRET_KEY), algorithms=[cached_settings.ALGORITHM]
        )

    @classmethod
    def decode_and_create(cls, token: str):
        decoded_token = cls.decode(token)
        return cls(**decoded_token)


class AccessToken(RefreshToken):
    pass


class Token(BaseModel):
    access_token: SecretStr
    refresh_token: SecretStr | None = None
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


class TokenData(BaseModel):
    id: UUID4 | None = None
    username: str | None = None
    exp: Union[Type[float], datetime] = confloat(gt=datetime.utcnow().timestamp())
