# -*- coding: utf-8 -*-
"""Security rest-api handlers."""

from fastapi import APIRouter, Depends, Form, status
from fastapi.responses import RedirectResponse, Response

from core import cached_settings
from core.database import UserGinoModel
from core.schemas import Token, UserViewModel
from core.services.security import (
    get_current_user_gino_obj,
    get_user_for_refresh_gino_obj,
    google_auth,
    login,
)

security_router = APIRouter(redirect_slashes=True, tags=["security"])


@security_router.post("/swag_swap_token", response_model=Token, tags=["security"])
async def swag_swap_token(code: str = Form(...)):  # pragma: no cover
    """SwaggerUI swap-token page."""
    redirect_uri = (
        f"{cached_settings.API_LOCATION}{cached_settings.SWAG_SWAP_TOKEN_ENDPOINT}"
    )
    return await google_auth(code=code, redirect_uri=redirect_uri)


@security_router.get("/react_swap_token", response_model=Token, tags=["security"])
async def react_swap_token(code: str):  # pragma: no cover
    """React client-app swap-token page."""
    redirect_uri = (
        f"{cached_settings.API_LOCATION}{cached_settings.REACT_SWAP_TOKEN_ENDPOINT}"
    )
    token_info = await google_auth(code=code, redirect_uri=redirect_uri)
    access_token = token_info["access_token"] if token_info else None
    frontend_url = f"{cached_settings.FRONTEND_AUTH_URL}={access_token}"
    return RedirectResponse(url=frontend_url)


@security_router.post("/refresh_access_token", response_model=Token, tags=["security"])
async def refresh_access_token(
    current_user: UserGinoModel = Depends(get_user_for_refresh_gino_obj),
):
    return await current_user.create_token()


@security_router.get("/react_login", tags=["auth"])
async def react_login(state: str):
    """React-app login page."""
    redirect_uri = (
        f"{cached_settings.API_LOCATION}{cached_settings.REACT_SWAP_TOKEN_ENDPOINT}"
    )
    authorization_url = await login(state=state, redirect_url=redirect_uri)
    return RedirectResponse(url=authorization_url)


@security_router.get("/swag_login", tags=["auth"])
async def swag_login(state: str):
    """SwaggerUI login page."""
    redirect_uri = (
        f"{cached_settings.API_LOCATION}{cached_settings.SWAG_SWAP_TOKEN_ENDPOINT}"
    )
    authorization_url = await login(state=state, redirect_url=redirect_uri)
    return RedirectResponse(url=authorization_url)


@security_router.get("/logout", tags=["auth"])
async def logout(
    current_user: UserGinoModel = Depends(get_current_user_gino_obj),
):
    await current_user.delete_refresh_token()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@security_router.get("/user/info", response_model=UserViewModel)
async def user_info(
    current_user: UserGinoModel = Depends(get_current_user_gino_obj),
):
    return current_user
