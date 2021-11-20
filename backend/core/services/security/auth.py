# -*- coding: utf-8 -*-
"""Authentication system."""
from typing import Any, Dict, Tuple

from fastapi import Depends
from fastapi.security.oauth2 import OAuth2AuthorizationCodeBearer
from google.auth.transport import requests
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow as GFlow
from jose import JWTError
from oauthlib.oauth2 import OAuth2Error
from pydantic import UUID4

from core.config import (
    GOOGLE_CLIENT_SECRETS_JSON,
    GOOGLE_SCOPES,
    SWAG_LOGIN_ENDPOINT,
    SWAG_SWAP_TOKEN_ENDPOINT,
)
from core.database import (
    ProductGinoModel,
    UserGinoModel,
    WishlistGinoModel,
    WishlistProductsGinoModel,
)
from core.schemas import AccessToken, GoogleIdInfo, RefreshToken
from core.utils import CREDENTIALS_EX, INACTIVE_EX, NOT_AN_OWNER, OAUTH2_EX

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=SWAG_LOGIN_ENDPOINT, tokenUrl=SWAG_SWAP_TOKEN_ENDPOINT
)


async def google_auth(code: str, redirect_uri: str) -> Dict[str, Any]:  # pragma: no cover
    """Check Google Auth code and create access token."""
    # Get authentication code
    flow = GFlow.from_client_secrets_file(
        GOOGLE_CLIENT_SECRETS_JSON, scopes=GOOGLE_SCOPES
    )
    flow.redirect_uri = redirect_uri
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


async def login(state: str, redirect_url: str) -> str:
    flow = GFlow.from_client_secrets_file(
        GOOGLE_CLIENT_SECRETS_JSON, scopes=GOOGLE_SCOPES
    )
    flow.redirect_uri = redirect_url
    flow_info: Tuple[str, str] = flow.authorization_url(
        access_type="offline", state=state, include_granted_scopes="true"
    )
    return flow_info[0]


async def get_or_create_user_gino_obj(id_info: GoogleIdInfo) -> UserGinoModel:
    """Get/Update or Create new user."""
    return await UserGinoModel.insert_or_update_by_ext_id(
        sub=id_info.sub,
        username=id_info.username,
        family_name=id_info.family_name,
        given_name=id_info.given_name,
        full_name=id_info.name,
    )


async def get_user_for_refresh_gino_obj(token: str):
    try:
        token_info = RefreshToken.decode_and_create(token=token)
        user = await UserGinoModel.get(token_info.id)
        if user is None or user.disabled:
            raise INACTIVE_EX
        token_valid = await user.token_is_valid(token)
        if not token_valid:
            raise CREDENTIALS_EX
    except (JWTError, ValueError):
        raise CREDENTIALS_EX
    return user


async def get_current_user_gino_obj(token: str = Depends(oauth2_scheme)):
    """Validate token and get user db model instance."""
    try:
        token_info = AccessToken.decode_and_create(token=token)
        user = await UserGinoModel.get(token_info.id)
        if user is None or user.disabled:
            raise INACTIVE_EX
    except (JWTError, ValueError):
        raise CREDENTIALS_EX
    return user


async def get_wishlist_gino_obj(id: UUID4):
    """Return WishlistGinoModel instance."""
    # TODO: ref view_query
    wishlist = await WishlistGinoModel.get_or_404(id)
    return await wishlist.view_query(wishlist.id)


async def get_product_gino_obj(id: UUID4):
    """Return ProductGinoModel instance."""
    # TODO: ref view_query
    product = await ProductGinoModel.get_or_404(id)
    return await product.view_query(product.id)


async def get_user_wishlist_gino_obj(
    wishlist: WishlistGinoModel = Depends(get_wishlist_gino_obj),
    current_user: UserGinoModel = Depends(get_current_user_gino_obj),
) -> WishlistGinoModel:
    """Return WishlistGinoModel if user has rights on it."""
    if current_user.superuser or wishlist.user_id == current_user.id:
        return wishlist
    raise NOT_AN_OWNER


async def get_user_product_gino_obj(
    product: ProductGinoModel = Depends(get_product_gino_obj),
    current_user: UserGinoModel = Depends(get_current_user_gino_obj),
) -> ProductGinoModel:
    """Return ProductGinoModel if user has rights on it."""
    if current_user.superuser or product.user_id == current_user.id:
        return product
    raise NOT_AN_OWNER


async def get_wishlist_product_gino_obj(id: UUID4):
    """Return WishlistProductsGinoModel instance."""
    return await WishlistProductsGinoModel.get_or_404(id)


async def get_user_wishlist_product_gino_obj(
    wishlist_product: WishlistProductsGinoModel = Depends(get_wishlist_product_gino_obj),
    current_user: UserGinoModel = Depends(get_current_user_gino_obj),
):
    """Return WishlistProductsGinoModel if user has rights on it."""
    wishlist = await WishlistGinoModel.get_or_404(wishlist_product.wishlist_id)
    if current_user.superuser or wishlist.user_id == current_user.id:
        return wishlist_product
    raise NOT_AN_OWNER
