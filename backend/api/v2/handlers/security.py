from fastapi import APIRouter, Depends, Response, status
from fastapi.security import OAuth2PasswordRequestForm

from core.database.models import UserGinoModel
from core.schemas import Token, UserCreateModel, UserViewModel
from core.services.security import (
    authenticate_user,
    get_active_user_by_refresh_token,
    get_current_active_user_by_access_token,
)

local_security_router = APIRouter(redirect_slashes=True, tags=["security"])


@local_security_router.post("/users/create", response_model=UserViewModel)
async def create_user(user_data: UserCreateModel):
    return await UserGinoModel.create(
        username=user_data.username, password=user_data.password
    )


@local_security_router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user: UserGinoModel = await authenticate_user(form_data.username, form_data.password)
    return await user.create_token()


@local_security_router.post("/token/refresh", response_model=Token)
async def refresh_access_token(
    current_user: UserGinoModel = Depends(get_active_user_by_refresh_token),
):
    return await current_user.create_token()


@local_security_router.get("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(
    current_user: UserGinoModel = Depends(get_current_active_user_by_access_token),
):
    await current_user.delete_refresh_token()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@local_security_router.get("/user/info", response_model=UserViewModel)
async def user_info(
    current_user: UserGinoModel = Depends(get_current_active_user_by_access_token),
):
    return current_user
