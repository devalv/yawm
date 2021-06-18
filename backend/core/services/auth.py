# -*- coding: utf-8 -*-
"""Authentication system."""

from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security.oauth2 import (
    OAuth2,
    OAuthFlowsModel,
    get_authorization_scheme_param,
)
from jose import JWTError, jwt

from core.config import SECRET_KEY, ALGORITHM
from core.database import UserGinoModel
from core.schemas import UserDBDataModel, TokenData

from starlette.requests import Request
from typing import Optional
from datetime import datetime, timedelta

# import jwt
# # from jwt import PyJWTError

from fastapi import Depends, FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.security.oauth2 import (
    OAuth2,
    OAuthFlowsModel,
    get_authorization_scheme_param,
)
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi

from starlette.status import HTTP_403_FORBIDDEN
from starlette.responses import RedirectResponse, JSONResponse, HTMLResponse
from starlette.requests import Request

from pydantic import BaseModel

import httplib2
from oauth2client import client
from google.oauth2 import id_token
from google.auth.transport import requests


class OAuth2PasswordBearerCookie(OAuth2):
    def __init__(
        self,
        tokenUrl: str,
        scheme_name: str = None,
        scopes: dict = None,
        auto_error: bool = True,
    ):
        if not scopes:
            scopes = {}
        flows = OAuthFlowsModel(password={"tokenUrl": tokenUrl, "scopes": scopes})
        super().__init__(flows=flows, scheme_name=scheme_name, auto_error=auto_error)

    async def __call__(self, request: Request) -> Optional[str]:
        print('calling yoba')
        print('request headers:', request.headers)
        header_authorization: str = request.headers.get("Authorization")
        cookie_authorization: str = request.cookies.get("Authorization")

        header_scheme, header_param = get_authorization_scheme_param(
            header_authorization
        )
        cookie_scheme, cookie_param = get_authorization_scheme_param(
            cookie_authorization
        )

        if header_scheme.lower() == "bearer":
            authorization = True
            scheme = header_scheme
            param = header_param

        # elif cookie_scheme.lower() == "bearer":
        #     authorization = True
        #     scheme = cookie_scheme
        #     param = cookie_param

        else:
            authorization = False

        print('header scheme:', header_scheme)
        print('header_param:', header_param)

        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                raise HTTPException(
                    status_code=HTTP_403_FORBIDDEN, detail="Not authenticated"
                )
            else:
                return None
        print('Auth passed')
        return param


oauth2_scheme = OAuth2PasswordBearerCookie(tokenUrl="/token")


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_active_user(ext_id: str):
    # TODO: token validation should be later
    print('get current user')
    print('user ext id:', ext_id)
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    # print('A')
    # print('Token is:', token)
    #     try:
    #     payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    #     print('B')
    #     user_id: str = payload.get("sub")
    #     print('C')
    #     if user_id is None:
    #         raise credentials_exception
    #     print('D')
    #     token_data = TokenData(ext_id=user_id)
    #     print('E')
    # except JWTError as jwt_err:
    #     print("JWTError")
    #     print(jwt_err)
    #     raise credentials_exception

    user = await UserGinoModel.query.where(UserGinoModel.ext_id == ext_id).gino.first()
    print('user:', user)
    if user is None or user.disabled:
        raise credentials_exception
    print('return user')
    return user


# async def get_current_active_user(current_user: UserDBDataModel = Depends(get_current_user)):
#     print('get current active user')
#     # if current_user.data.attributes.disabled:
#     #     raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user


async def get_yoba_user(token: str = Depends(oauth2_scheme)):
# async def get_yoba_user(token: str):
    # print('token is:', args)
    # print('token is:', kwargs)
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    print('A')
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        ext_id: str = payload.get("sub")
        if ext_id is None:
            raise credentials_exception
        token_data = TokenData(ext_id=ext_id)
        print('B')
    except JWTError as ex:
        print('hwt err:', ex)
        raise credentials_exception
    user = await UserGinoModel.query.where(UserGinoModel.ext_id == ext_id).gino.first()
    if user is None:
        raise credentials_exception
    return user


async def get_yoba_active_user(current_user: UserDBDataModel = Depends(get_yoba_user)):
    print('ABC')
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
