# -*- coding: utf-8 -*-
"""Security rest-api handlers."""

from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OpenIdConnect
from fastapi.encoders import jsonable_encoder
from jose import JWTError, jwt
from fastapi.responses import RedirectResponse

from starlette.status import HTTP_403_FORBIDDEN
from starlette.responses import (
    RedirectResponse,
    JSONResponse,
    HTMLResponse,
)
from starlette.requests import Request

import httplib2

from google.oauth2 import id_token
from google.auth.transport import requests

from core.config import (
    ACCESS_TOKEN_EXPIRE_MIN,
    API_DOMAIN,
    API_PORT,
    GOOGLE_CLIENT_ID,
    GOOGLE_CLIENT_SECRETS_JSON,
    ALGORITHM,
    SWAP_TOKEN_ENDPOINT,
    LOGIN_ENDPOINT,
    GOOGLE_SCOPES
)
from core.schemas.security import (
    UserDBModel,
    TokenData,
    Token,
)

from core.services.auth import get_current_active_user, create_access_token, get_yoba_active_user


security_router = APIRouter(prefix="", redirect_slashes=True, tags=["auth"])

API_LOCATION = f"http://{API_DOMAIN}:{API_PORT}"

SUCCESS_ROUTE = "/api/v1/users/me"
ERROR_ROUTE = "/api/v1/login_error"


@security_router.get(f"{LOGIN_ENDPOINT}")
async def login():
    print('start login')
    import google.oauth2.credentials
    import google_auth_oauthlib.flow

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        GOOGLE_CLIENT_SECRETS_JSON,
        scopes=[
                "https://www.googleapis.com/auth/userinfo.profile"])
    print('A1')
    flow.redirect_uri = f"{API_LOCATION}{SWAP_TOKEN_ENDPOINT}"
    print('A2')

    authorization_url, state = flow.authorization_url(
        # Enable offline access so that you can refresh an access token without
        # re-prompting the user for permission. Recommended for web server apps.
        access_type='offline',
        # Enable incremental authorization. Recommended as a best practice.
        include_granted_scopes='false')
    print('A3')
    return RedirectResponse(url=authorization_url)


@security_router.post(f"{SWAP_TOKEN_ENDPOINT}", response_model=Token, tags=["security"])
async def swap_token(request: Request = None):
    # if not request.headers.get("X-Requested-With"):
    #     raise HTTPException(status_code=400, detail="Incorrect headers")

    # TODO: use for extra client checking?
    # google_client_type = request.headers.get("X-Google-OAuth2-Type")
    print('swap token')
    print('SWAPSWAPSWAP')

    print('request:', request)
    import google.oauth2.credentials
    import google_auth_oauthlib.flow
    from google.auth import crypt
    from google.auth import jwt

    # state = flask.session['state']

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        GOOGLE_CLIENT_SECRETS_JSON,
        scopes=[
                "https://www.googleapis.com/auth/userinfo.profile"])
    flow.redirect_uri = flow.redirect_uri = f"{API_LOCATION}{SWAP_TOKEN_ENDPOINT}"

    # Use the authorization server's response to fetch the OAuth 2.0 tokens.
    body_bytes = await request.body()
    body_uni = jsonable_encoder(body_bytes)
    for el in body_uni.split("&"):
        if el.startswith("code="):
            auth_code = el.replace("code=", "").replace("%2F", "/")

    print('auth code:', auth_code)
    # print('auth code:', auth_code)
    # auth_code = auth_code.replace("%2F", "/")
    # print('auth code:', auth_code)

    # flow.fetch_token(code=auth_code)
    flow.fetch_token(code=auth_code)
    print('token fetched')
    # Store credentials in the session.
    # ACTION ITEM: In a production app, you likely want to save these
    #              credentials in a persistent database instead.
    credentials = flow.credentials

    cred_dict = {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes}

    # raise ValueError
    # authenticated_user = await get_current_active_user(google_user_id)
    #
    print('cred dict:', cred_dict)

    print('id token', credentials.id_token)
    # TODO: token validation https://developers.google.com/identity/protocols/oauth2/openid-connect
    from core.config import GOOGLE_CERT_KEYS
    # TODO: add aud check
    # claims = jwt.decode(credentials.id_token, certs=GOOGLE_CERT_KEYS)
    claims = jwt.decode(credentials.id_token, certs=GOOGLE_CERT_KEYS, verify=False)

    print('decoded:', claims)
    google_user_id = claims['sub']

    authenticated_user = await get_current_active_user(google_user_id)
    print('authenticated user:', authenticated_user)
    if not authenticated_user:
        raise HTTPException(status_code=400, detail="Incorrect email address")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MIN)
    access_token = create_access_token(
        data={"sub": authenticated_user.ext_id,
              "username": authenticated_user.username,
              },
        expires_delta=access_token_expires
    )
    print('access token:', access_token)
    token = jsonable_encoder(access_token)
    print('token:', token)

    response = JSONResponse(
        {"access_token": token, "token_type": "bearer", "alg": ALGORITHM,
         "typ": "JWT"})

    print({"token": token,
           "token_type": "bearer",
           "alg": ALGORITHM,
           "typ": "JWT"})
    # return
    return response


@security_router.get(f"{ERROR_ROUTE}", tags=["security"])
async def login_error():
    return "Something went wrong logging in!"


@security_router.get(f"{SUCCESS_ROUTE}", response_model=UserDBModel)
async def read_users_me(current_user: UserDBModel = Depends(get_yoba_active_user)):
    print('Read users')
    print('current user')
    print(current_user)
    return current_user
