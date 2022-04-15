from typing import Any

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from pydantic import UUID4

from core.database import (
    ProductGinoModel,
    UserGinoModel,
    WishlistGinoModel,
    WishlistProductsGinoModel,
)
from core.schemas import TokenData
from core.utils import CREDENTIALS_EX, INACTIVE_EX, NOT_AN_OWNER

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v2/token")


async def authenticate_user(username: str, password: str) -> UserGinoModel:
    user: UserGinoModel = await UserGinoModel.query.where(
        UserGinoModel.username == username
    ).gino.first()

    if not user:
        raise CREDENTIALS_EX

    if not user.verify_password(password):
        raise CREDENTIALS_EX

    if user.disabled:
        raise INACTIVE_EX

    return user


async def get_active_user_by_token(
    access_token: str | None = None, refresh_token: str | None = None
) -> UserGinoModel:
    """Get active User instance by access or refresh token."""
    if not access_token and not refresh_token:
        raise ValueError("Pass the access_token or refresh_token.")

    try:
        if access_token:
            token_data: TokenData = TokenData.decode(token=access_token)  # type: ignore
        else:
            token_data: TokenData = TokenData.decode(token=refresh_token)  # type: ignore

        if token_data.sub is None:
            raise CREDENTIALS_EX
    except (JWTError, NameError):
        raise CREDENTIALS_EX

    user: UserGinoModel = await UserGinoModel.get(token_data.sub)
    if user is None:
        raise CREDENTIALS_EX

    if user.disabled:
        raise INACTIVE_EX

    return user


async def get_active_user_by_refresh_token(token: str) -> UserGinoModel:
    """Get active User instance by refresh token."""
    active_user = await get_active_user_by_token(refresh_token=token)
    # Validate token
    token_valid: bool = await active_user.refresh_token_is_valid(token)
    if not token_valid:
        raise CREDENTIALS_EX
    return active_user


async def get_current_active_user_by_access_token(
    token: str = Depends(oauth2_scheme),
) -> UserGinoModel:
    """Get active User instance by access token."""
    return await get_active_user_by_token(access_token=token)


async def get_wishlist_gino_obj(id: UUID4) -> Any:
    """Return WishlistGinoModel instance."""
    # TODO: ref view_query
    wishlist: WishlistGinoModel = await WishlistGinoModel.get_or_404(id)
    return await wishlist.view_query(wishlist.id)


async def get_product_gino_obj(id: UUID4) -> Any:
    """Return ProductGinoModel instance."""
    # TODO: ref view_query
    product: ProductGinoModel = await ProductGinoModel.get_or_404(id)
    return await product.view_query(product.id)


async def get_user_wishlist_gino_obj(
    wishlist: WishlistGinoModel = Depends(get_wishlist_gino_obj),
    current_user: UserGinoModel = Depends(get_current_active_user_by_access_token),
) -> WishlistGinoModel:
    """Return WishlistGinoModel if user has rights on it."""
    if current_user.superuser or wishlist.user_id == current_user.id:
        return wishlist
    raise NOT_AN_OWNER


async def get_user_product_gino_obj(
    product: ProductGinoModel = Depends(get_product_gino_obj),
    current_user: UserGinoModel = Depends(get_current_active_user_by_access_token),
) -> ProductGinoModel:
    """Return ProductGinoModel if user has rights on it."""
    if current_user.superuser or product.user_id == current_user.id:
        return product
    raise NOT_AN_OWNER


async def get_wishlist_product_gino_obj(id: UUID4) -> Any:
    """Return WishlistProductsGinoModel instance."""
    return await WishlistProductsGinoModel.get_or_404(id)


async def get_user_wishlist_product_gino_obj(
    wishlist_product: WishlistProductsGinoModel = Depends(get_wishlist_product_gino_obj),
    current_user: UserGinoModel = Depends(get_current_active_user_by_access_token),
) -> WishlistProductsGinoModel:
    """Return WishlistProductsGinoModel if user has rights on it."""
    wishlist = await WishlistGinoModel.get_or_404(wishlist_product.wishlist_id)
    if current_user.superuser or wishlist.user_id == current_user.id:
        return wishlist_product
    raise NOT_AN_OWNER
