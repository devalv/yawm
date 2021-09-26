# -*- coding: utf-8 -*-
"""Authentication system."""

from fastapi import Depends
from fastapi.security.oauth2 import OAuth2AuthorizationCodeBearer
from jose import JWTError
from pydantic import UUID4

from core.config import LOGIN_ENDPOINT, SWAP_TOKEN_ENDPOINT
from core.database import ProductGinoModel, UserGinoModel, WishlistGinoModel
from core.schemas import AccessToken, GoogleIdInfo, RefreshToken
from core.utils import CREDENTIALS_EX, INACTIVE_EX, NOT_AN_OWNER

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=LOGIN_ENDPOINT, tokenUrl=SWAP_TOKEN_ENDPOINT
)


async def get_or_create_user_gino_obj(id_info: GoogleIdInfo):
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


async def get_current_user_gino_obj(token: str = Depends(oauth2_scheme)):  # noqa: B008
    """Validate token and get user db model instance."""
    try:
        token_info = AccessToken.decode_and_create(token=token)
        user = await UserGinoModel.get(token_info.id)
        if user is None or user.disabled:
            raise INACTIVE_EX
    except (JWTError, ValueError):
        raise CREDENTIALS_EX
    return user


async def get_wishlist_gino_obj(id: UUID4):  # noqa: A002
    """Return WishlistGinoModel instance."""
    # TODO: ref view_query
    wishlist = await WishlistGinoModel.get_or_404(id)
    return await wishlist.view_query(wishlist.id)


async def get_product_gino_obj(id: UUID4):  # noqa: A002
    """Return ProductGinoModel instance."""
    # TODO: ref view_query
    product = await ProductGinoModel.get_or_404(id)
    return await product.view_query(product.id)


async def get_user_wishlist_gino_obj(
    wishlist: WishlistGinoModel = Depends(get_wishlist_gino_obj),  # noqa: B008
    current_user: UserGinoModel = Depends(get_current_user_gino_obj),  # noqa: B008
) -> WishlistGinoModel:
    """Return WishlistGinoModel if user has rights on it."""
    if current_user.superuser or wishlist.user_id == current_user.id:
        return wishlist
    raise NOT_AN_OWNER


async def get_user_product_gino_obj(
    product: ProductGinoModel = Depends(get_product_gino_obj),  # noqa: B008
    current_user: UserGinoModel = Depends(get_current_user_gino_obj),  # noqa: B008
) -> ProductGinoModel:
    """Return ProductGinoModel if user has rights on it."""
    if current_user.superuser or product.user_id == current_user.id:
        return product
    raise NOT_AN_OWNER
