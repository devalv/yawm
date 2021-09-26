# -*- coding: utf-8 -*-
"""Security rest-api handlers."""

from fastapi import APIRouter, Depends, Form, status
from fastapi.responses import RedirectResponse
from google.auth.transport import requests
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow as GFlow
from oauthlib.oauth2 import OAuth2Error

from core.config import (
    API_LOCATION,
    GOOGLE_CLIENT_SECRETS_JSON,
    GOOGLE_SCOPES,
    SWAP_TOKEN_ENDPOINT,
)
from core.database import UserGinoModel
from core.schemas import GoogleIdInfo, Token, UserViewModel
from core.services.security import (
    get_current_user_gino_obj,
    get_or_create_user_gino_obj,
    get_user_for_refresh_gino_obj,
)
from core.utils import CREDENTIALS_EX, OAUTH2_EX

security_router = APIRouter(redirect_slashes=True, tags=["security"])


@security_router.post("/swap_token", response_model=Token, tags=["security"])
async def swap_token(code: str = Form(...)):  # pragma: no cover  # noqa: B008
    """Check Google Auth code and create access token."""
    # Get authentication code
    flow = GFlow.from_client_secrets_file(
        GOOGLE_CLIENT_SECRETS_JSON, scopes=GOOGLE_SCOPES
    )
    flow.redirect_uri = f"{API_LOCATION}{SWAP_TOKEN_ENDPOINT}"
    try:
        flow.fetch_token(code=code)
    except OAuth2Error:
        raise OAUTH2_EX
    else:
        credentials = flow.credentials
    # token validation
    try:
        # TODO: @devalv change requests.Request() to httpx.Request or local validation
        id_info = id_token.verify_oauth2_token(
            credentials.id_token, requests.Request(), credentials.client_id
        )
        id_info = GoogleIdInfo(**id_info)
    except ValueError:
        raise CREDENTIALS_EX
    # get user object
    authenticated_user = await get_or_create_user_gino_obj(id_info)
    # generate system token for a user
    return await authenticated_user.create_token()


@security_router.post("/refresh_access_token", response_model=Token, tags=["security"])
async def refresh_access_token(
    current_user: UserGinoModel = Depends(get_user_for_refresh_gino_obj),  # noqa: B008
):
    return await current_user.create_token()


@security_router.get("/login", tags=["auth"])
async def login(state: str):
    flow = GFlow.from_client_secrets_file(
        GOOGLE_CLIENT_SECRETS_JSON, scopes=GOOGLE_SCOPES
    )
    flow.redirect_uri = f"{API_LOCATION}{SWAP_TOKEN_ENDPOINT}"
    authorization_url, frontend_state = flow.authorization_url(
        access_type="offline", state=state, include_granted_scopes="true"
    )

    return RedirectResponse(url=authorization_url)


@security_router.get("/logout", status_code=status.HTTP_204_NO_CONTENT, tags=["auth"])
async def logout(
    current_user: UserGinoModel = Depends(get_current_user_gino_obj),  # noqa: B008
):
    await current_user.delete_refresh_token()


@security_router.get("/user/info", response_model=UserViewModel)
async def user_info(
    current_user: UserGinoModel = Depends(get_current_user_gino_obj),  # noqa: B008
):
    return current_user
