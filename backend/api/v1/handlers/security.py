# -*- coding: utf-8 -*-
"""Security rest-api handlers."""

from datetime import timedelta

from fastapi import APIRouter, Form, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from fastapi_versioning import version

from google.auth.transport import requests
from google.oauth2 import id_token

from google_auth_oauthlib.flow import Flow as GFlow

from core.config import (
    ACCESS_TOKEN_EXPIRE_MIN,
    ALGORITHM,
    API_LOCATION,
    GOOGLE_CLIENT_SECRETS_JSON,
    GOOGLE_SCOPES,
    SWAP_TOKEN_ENDPOINT,
)
from core.schemas.security import Token
from core.services.security import create_access_token, get_current_active_user


security_router = APIRouter(redirect_slashes=True, tags=["auth"])


# TODO: refresh_token == security
# TODO: swap_token == security


@security_router.post("/swap_token", response_model=Token, tags=["security"])
@version(1)
async def swap_token(code: str = Form(...)):  # noqa: B008, D103

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # TODO: refresh token in the system
    # TODO: 500err when page need to be reloaded

    # Get authentication code
    flow = GFlow.from_client_secrets_file(
        GOOGLE_CLIENT_SECRETS_JSON, scopes=GOOGLE_SCOPES
    )
    flow.redirect_uri = f"{API_LOCATION}{SWAP_TOKEN_ENDPOINT}"

    flow.fetch_token(code=code)
    credentials = flow.credentials

    # token validation
    try:
        # TODO: change requests.Request() to httpx.Request
        id_info = id_token.verify_oauth2_token(
            credentials.id_token, requests.Request(), credentials.client_id
        )

        google_user_id = id_info["sub"]
    except ValueError:
        raise credentials_exception

    # another section
    authenticated_user = await get_current_active_user(google_user_id)
    if not authenticated_user:
        # TODO: user registration?
        raise HTTPException(status_code=400, detail="Incorrect user id")
    # generate system token for a user
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MIN)
    access_token = create_access_token(
        data={
            "sub": authenticated_user.ext_id,
            "username": authenticated_user.username,
        },
        expires_delta=access_token_expires,
    )
    token = jsonable_encoder(access_token)
    return JSONResponse(
        {"access_token": token, "token_type": "bearer", "alg": ALGORITHM, "typ": "JWT"}
    )
