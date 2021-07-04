# -*- coding: utf-8 -*-
"""Auth rest-api handlers."""

from fastapi import APIRouter, Depends, status
from fastapi.responses import RedirectResponse
from fastapi_versioning import version
from google_auth_oauthlib.flow import Flow as GFlow

from core.config import (
    API_LOCATION,
    GOOGLE_CLIENT_SECRETS_JSON,
    GOOGLE_SCOPES,
    SWAP_TOKEN_ENDPOINT,
)
from core.schemas.security import UserDBModel
from core.services.security import get_current_user

auth_router = APIRouter(redirect_slashes=True, tags=["auth"])


@auth_router.get("/login", tags=["auth"])
@version(1)
async def login(state: str):
    flow = GFlow.from_client_secrets_file(
        GOOGLE_CLIENT_SECRETS_JSON, scopes=GOOGLE_SCOPES
    )
    flow.redirect_uri = f"{API_LOCATION}{SWAP_TOKEN_ENDPOINT}"
    authorization_url, frontend_state = flow.authorization_url(
        access_type="offline", state=state, include_granted_scopes="true"
    )

    return RedirectResponse(url=authorization_url)


@auth_router.get("/logout", status_code=status.HTTP_204_NO_CONTENT, tags=["auth"])
@version(1)
async def logout(current_user: UserDBModel = Depends(get_current_user)):  # noqa: B008
    await current_user.delete_refresh_token()


@auth_router.get("/user/info", response_model=UserDBModel)
@version(1)
async def user_info(
    current_user: UserDBModel = Depends(get_current_user),  # noqa: B008
):
    return current_user
