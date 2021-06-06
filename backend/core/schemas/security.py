# -*- coding: utf-8 -*-
"""Pydantic security models."""

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str = None
    email: str = None


class User(BaseModel):
    username: str
    email: str = None
    full_name: str = None
    disabled: bool = None
    family_name: str = None
    given_name: str = None
    picture: str = None

    # sub - Google user id
    # print('sub:', credentials.id_token['sub'])
    # print('email:', credentials.id_token['email'])
    # print('name:', credentials.id_token.get('name', None))
    # print('picture:', credentials.id_token.get('picture', None))
    # print('given_name:', credentials.id_token.get('given_name', None))
    # print('family_name:', credentials.id_token.get('family_name', None))
