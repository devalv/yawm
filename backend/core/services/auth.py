# -*- coding: utf-8 -*-
"""Authentication system."""

from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt

from core.config import SECRET_KEY, ALGORITHM
from core.database import UserGinoModel
from core.schemas import UserDBDataModel, TokenData
from typing import Optional
from datetime import datetime, timedelta


from fastapi import Depends, HTTPException

from core.config import API_DOMAIN, API_PORT, SWAP_TOKEN_ENDPOINT, GOOGLE_SCOPES, GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, LOGIN_ENDPOINT

from fastapi.security.oauth2 import OAuth2AuthorizationCodeBearer

google_auth_url = f"https://accounts.google.com/o/oauth2/v2/auth"

# OAuthFlowImplicit
# OAuth2AuthorizationCodeBearer
# OAuth2

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    # authorizationUrl=google_auth_url,
    # tokenUrl="https://www.googleapis.com/oauth2/v4/token",
    authorizationUrl=LOGIN_ENDPOINT,
    tokenUrl=SWAP_TOKEN_ENDPOINT,
    scopes=GOOGLE_SCOPES
)


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
    # TODO: new user registtration
    return user


# async def get_current_active_user(current_user: UserDBDataModel = Depends(get_current_user)):
#     print('get current active user')
#     # if current_user.data.attributes.disabled:
#     #     raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user


async def get_yoba_user(token: str = Depends(oauth2_scheme)):

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
