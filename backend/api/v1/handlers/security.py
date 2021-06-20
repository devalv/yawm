# -*- coding: utf-8 -*-
"""Security rest-api handlers."""

from datetime import timedelta

from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import RedirectResponse, JSONResponse

from starlette.requests import Request

import google_auth_oauthlib.flow
from google.auth import jwt

from core.config import (
    ACCESS_TOKEN_EXPIRE_MIN,
    API_DOMAIN,
    API_PORT,
    GOOGLE_CLIENT_SECRETS_JSON,
    ALGORITHM,
    SWAP_TOKEN_ENDPOINT,
    LOGIN_ENDPOINT,
    GOOGLE_SCOPES,
    GOOGLE_CERT_KEYS
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
async def login(state: str):
    print('incoming state:', state)
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        GOOGLE_CLIENT_SECRETS_JSON,
        scopes=GOOGLE_SCOPES)
    flow.redirect_uri = f"{API_LOCATION}{SWAP_TOKEN_ENDPOINT}"

    authorization_url, yboa_state = flow.authorization_url(
        access_type='offline',
        # response_type='code',
        state=state,
        include_granted_scopes='true')

    print('Login state:', yboa_state)

    return RedirectResponse(url=authorization_url)


@security_router.post(f"{SWAP_TOKEN_ENDPOINT}", response_model=Token, tags=["security"])
async def swap_token(request: Request = None):
    # TODO: 500err when page need to be reloaded
    # if not request.headers.get("X-Requested-With"):
    #     raise HTTPException(status_code=400, detail="Incorrect headers")

    # TODO: use for extra client checking?
    # google_client_type = request.headers.get("X-Google-OAuth2-Type")

    # TODO: Auth WarningAuthorization may be unsafe, passed state was changed in
    #  server Passed state wasn't returned from auth server

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        GOOGLE_CLIENT_SECRETS_JSON,
        scopes=GOOGLE_SCOPES)
    flow.redirect_uri = f"{API_LOCATION}{SWAP_TOKEN_ENDPOINT}"

    # Use the authorization server's response to fetch the OAuth 2.0 tokens.
    body_bytes = await request.body()
    body_uni = jsonable_encoder(body_bytes)
    # TODO: set response type only as code
    for el in body_uni.split("&"):
        if el.startswith("code="):
            auth_code = el.replace("code=", "").replace("%2F", "/")

    flow.fetch_token(code=auth_code)

    credentials = flow.credentials
    print(dir(credentials))

    claims = jwt.decode(credentials.id_token, certs=GOOGLE_CERT_KEYS, verify=True)

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
    token = jsonable_encoder(access_token)

    response = JSONResponse(
        {"access_token": token,
         "token_type": "bearer",
         "alg": ALGORITHM,
         "typ": "JWT"})

    print({"token": token,
           "token_type": "bearer",
           "alg": ALGORITHM,
           "typ": "JWT"})

    return response


@security_router.get(f"{ERROR_ROUTE}", tags=["security"])
async def login_error():
    return "Something went wrong logging in!"


@security_router.get(f"{SUCCESS_ROUTE}", response_model=UserDBModel)
async def read_users_me(current_user: UserDBModel = Depends(get_yoba_active_user)):
    return current_user
