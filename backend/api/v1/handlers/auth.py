# -*- coding: utf-8 -*-
"""Auth rest-api handlers."""

from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse

from fastapi_versioning import version

from google_auth_oauthlib.flow import Flow as GFlow

from core.config import (
    API_LOCATION,
    GOOGLE_CLIENT_SECRETS_JSON,
    GOOGLE_SCOPES,
    SUCCESS_ROUTE,
    SWAP_TOKEN_ENDPOINT,
)
from core.schemas.security import UserDBModel
from core.services.security import get_yoba_user

auth_router = APIRouter(redirect_slashes=True, tags=["auth"])

ERROR_ROUTE = "/api/v1/login_error"

# TODO: login == auth
# TODO: logout == auth
# TODO: user info == auth


@auth_router.get("/login", tags=["auth"])
@version(1)
async def login(state: str):  # noqa: D103
    flow = GFlow.from_client_secrets_file(
        GOOGLE_CLIENT_SECRETS_JSON, scopes=GOOGLE_SCOPES
    )
    flow.redirect_uri = f"{API_LOCATION}{SWAP_TOKEN_ENDPOINT}"
    authorization_url, frontend_state = flow.authorization_url(
        access_type="offline", state=state, include_granted_scopes="true"
    )

    return RedirectResponse(url=authorization_url)


@auth_router.get(f"{ERROR_ROUTE}", tags=["auth"])
@version(1)
async def login_error():  # noqa: D103
    return "Something went wrong logging in!"


@auth_router.get(f"{SUCCESS_ROUTE}", response_model=UserDBModel)
@version(1)
async def read_users_me(  # noqa: D103
    current_user: UserDBModel = Depends(get_yoba_user),  # noqa: B008
):
    return current_user
