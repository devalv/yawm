# -*- coding: utf-8 -*-
"""Authentication system."""
from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2AuthorizationCodeBearer

from jose import JWTError, jwt

from core.config import ALGORITHM, LOGIN_ENDPOINT, SECRET_KEY, SWAP_TOKEN_ENDPOINT
from core.database import UserGinoModel
from core.schemas import TokenData, UserDBDataModel


google_auth_url = "https://accounts.google.com/o/oauth2/v2/auth"

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=LOGIN_ENDPOINT, tokenUrl=SWAP_TOKEN_ENDPOINT
)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):  # noqa
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt  # noqa


async def get_current_active_user(ext_id: str):  # noqa
    # TODO: token validation should be later
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # print('Token is:', token)  # noqa
    #     try:  # noqa
    #     payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])  # noqa
    #     user_id: str = payload.get("sub")  # noqa
    #     if user_id is None:  # noqa
    #         raise credentials_exception  # noqa
    #     token_data = TokenData(ext_id=user_id)  # noqa
    # except JWTError as jwt_err:  # noqa
    #     raise credentials_exception  # noqa

    user = await UserGinoModel.query.where(UserGinoModel.ext_id == ext_id).gino.first()
    if user is None or user.disabled:
        raise credentials_exception
    # TODO: new user registration
    return user


# async def get_current_active_user(current_user: UserDBDataModel = Depends(get_current_user)):  # noqa
#     # if current_user.data.attributes.disabled:  # noqa
#     #     raise HTTPException(status_code=400, detail="Inactive user")  # noqa
#     return current_user  # noqa


async def get_yoba_user(token: str = Depends(oauth2_scheme)):  # noqa
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        ext_id: str = payload.get("sub")
        if ext_id is None:
            raise credentials_exception
        token_data = TokenData(ext_id=ext_id)  # noqa
    except JWTError as ex:  # noqa
        raise credentials_exception
    user = await UserGinoModel.query.where(UserGinoModel.ext_id == ext_id).gino.first()
    if user is None:
        raise credentials_exception
    return user


async def get_yoba_active_user(  # noqa
    current_user: UserDBDataModel = Depends(get_yoba_user),  # noqa
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
