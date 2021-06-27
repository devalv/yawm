# -*- coding: utf-8 -*-
"""Security rest-api handlers."""

from fastapi import APIRouter, Form

from fastapi_versioning import version

from google.auth.transport import requests
from google.oauth2 import id_token

from google_auth_oauthlib.flow import Flow as GFlow

from core.config import (
    ALGORITHM,
    API_LOCATION,
    GOOGLE_CLIENT_SECRETS_JSON,
    GOOGLE_SCOPES,
    SWAP_TOKEN_ENDPOINT,
)
from core.schemas.security import GoogleIdInfo, Token
from core.services.security import get_or_create_user
from core.utils import CREDENTIALS_EX


security_router = APIRouter(redirect_slashes=True, tags=["auth"])


# TODO: refresh_token == security
# TODO: swap_token == security


@security_router.post("/swap_token", response_model=Token, tags=["security"])
@version(1)
async def swap_token(code: str = Form(...)):  # noqa: B008, D103
    # TODO: return Token
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
        # TODO: change requests.Request() to httpx.Request or local validation
        id_info = id_token.verify_oauth2_token(
            credentials.id_token, requests.Request(), credentials.client_id
        )
        id_info = GoogleIdInfo(**id_info)
    except ValueError:
        raise CREDENTIALS_EX

    # another section
    authenticated_user = await get_or_create_user(id_info)

    # generate system token for a user
    token = authenticated_user.create_access_token()

    return {
        "access_token": token,
        "token_type": "bearer",
        "alg": ALGORITHM,
        "typ": "JWT",
    }
