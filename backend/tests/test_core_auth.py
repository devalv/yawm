from datetime import datetime, timedelta
from time import sleep
from typing import Any, Dict
from uuid import uuid4

import pytest
import pytest_asyncio
from fastapi import HTTPException, status
from jose import jwt

from core import cached_settings
from core.database import TokenInfoGinoModel, UserGinoModel
from core.services.security.auth import (
    authenticate_user,
    get_active_user_by_refresh_token,
    get_active_user_by_token,
)

pytestmark = [
    pytest.mark.asyncio,
    pytest.mark.api_full,
    pytest.mark.security,
]


API_URL_PREFIX = "/api/v2"


@pytest_asyncio.fixture
async def token_data(single_admin) -> Dict[str, Any]:
    return {
        "exp": datetime.utcnow()
        + timedelta(minutes=cached_settings.ACCESS_TOKEN_EXPIRE_MIN),  # noqa: W503
        "sub": single_admin.id_str,
        "username": single_admin.username,
    }


@pytest_asyncio.fixture
async def bad_token(token_data) -> Dict[str, Any]:
    return {
        "access_token": jwt.encode(
            token_data, "qwe", algorithm=cached_settings.ALGORITHM
        ),
        "refresh_token": jwt.encode(
            token_data, "qwe", algorithm=cached_settings.ALGORITHM
        ),
        "token_type": "bearer",
        "alg": cached_settings.ALGORITHM,
        "typ": "JWT",
    }


@pytest_asyncio.fixture
async def bad_access_token(bad_token) -> str:
    return bad_token["access_token"]


@pytest_asyncio.fixture
async def no_refresh_token(single_admin):
    token = await TokenInfoGinoModel.get(single_admin.id)
    await token.delete()


@pytest_asyncio.fixture
async def single_admin_refresh_token(single_admin_token) -> str:
    return single_admin_token["refresh_token"]


@pytest_asyncio.fixture
async def single_disabled_admin_token(single_admin_access_token, single_admin) -> str:
    await single_admin.update(disabled=True).apply()
    return single_admin_access_token


@pytest_asyncio.fixture
async def single_disabled_refresh_token(single_admin_refresh_token, single_admin) -> str:
    await single_admin.update(disabled=True).apply()
    return single_admin_refresh_token


async def test_logout(backend_app, single_admin_auth_headers):
    resp = await backend_app.get(
        f"{API_URL_PREFIX}/logout", headers=single_admin_auth_headers
    )
    assert resp.status_code == status.HTTP_204_NO_CONTENT


async def test_logout_2(backend_app):
    resp = await backend_app.get(f"{API_URL_PREFIX}/logout")
    assert resp.status_code == status.HTTP_401_UNAUTHORIZED


class TestUser:
    """Authenticated user attributes tests."""

    async def test_granted_info(
        self, backend_app, single_admin, single_admin_auth_headers
    ):
        resp = await backend_app.get(
            f"{API_URL_PREFIX}/users/info", headers=single_admin_auth_headers
        )
        assert resp.status_code == status.HTTP_200_OK
        for key in resp.json():
            if key in {"created_at", "updated_at"}:
                continue
            assert hasattr(single_admin, key)
            value = getattr(single_admin, key)
            if key == "id":
                value = str(value)
            assert resp.json()[key] == value

    async def test_permitted_info(self, backend_app):
        resp = await backend_app.get(f"{API_URL_PREFIX}/users/info")
        assert resp.status_code == status.HTTP_401_UNAUTHORIZED

    async def test_user_create(self, backend_app):
        resp = await backend_app.post(
            f"{API_URL_PREFIX}/users/create",
            json={"username": "new-user", "password": "new-user-password"},
        )
        assert resp.status_code == status.HTTP_200_OK
        user_obj: UserGinoModel = await UserGinoModel.get_by_username("new-user")
        assert user_obj.active
        assert user_obj.superuser is False
        assert user_obj.verify_password("new-user-password")
        await user_obj.delete()

    async def test_user_create_bad_pass(self, backend_app):
        resp = await backend_app.post(
            f"{API_URL_PREFIX}/users/create",
            json={"username": "new-user", "password": "short"},
        )
        assert resp.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        user_obj: UserGinoModel = await UserGinoModel.get_by_username("new-user")
        assert not user_obj


class TestUserToken:
    async def test_login_for_access_token(self, backend_app, single_user: UserGinoModel):
        resp = await backend_app.post(
            f"{API_URL_PREFIX}/token",
            form={"username": single_user.username, "password": "test-user-password"},
        )
        assert resp.status_code == status.HTTP_200_OK
        resp_data = resp.json()
        assert "access_token" in resp_data
        assert "refresh_token" in resp_data

    async def test_refresh_access_token(
        self, backend_app, single_admin_refresh_token: str
    ):
        resp = await backend_app.post(
            f"{API_URL_PREFIX}/token/refresh",
            query_string={"token": single_admin_refresh_token},
        )
        assert resp.status_code == status.HTTP_200_OK
        resp_data = resp.json()
        assert "access_token" in resp_data
        assert "refresh_token" in resp_data

    async def test_refresh_access_token_with_bad_token(self, backend_app):
        resp = await backend_app.post(
            f"{API_URL_PREFIX}/token/refresh", query_string={"token": "qwe"}
        )
        assert resp.status_code == status.HTTP_401_UNAUTHORIZED

    async def test_get_active_user_by_refresh_token(
        self, backend_app, single_admin_refresh_token: str
    ):
        active_user: UserGinoModel = await get_active_user_by_refresh_token(
            single_admin_refresh_token
        )
        assert isinstance(active_user, UserGinoModel)

    async def test_get_active_user_by_bad_refresh_token(
        self, backend_app, single_user: UserGinoModel
    ):
        old_token: str = await single_user.create_refresh_token()
        sleep(1)
        new_token: str = await single_user.create_refresh_token()
        assert old_token != new_token
        try:
            await get_active_user_by_refresh_token(old_token)
        except HTTPException:
            assert True
        else:
            raise AssertionError("Token is bad. User should`t be received.")

    async def test_get_active_user_by_token_no_token(self, backend_app):
        try:
            await get_active_user_by_token()
        except ValueError:
            assert True
        else:
            raise AssertionError("No token was sent. User should`t be received.")

    async def test_get_active_user_by_token_with_no_sub(
        self, backend_app, single_user: UserGinoModel
    ):
        exp_time: datetime = datetime.utcnow() + timedelta(
            minutes=cached_settings.ACCESS_TOKEN_EXPIRE_MIN
        )
        bad_token_data = {
            "exp": exp_time,
            "username": single_user.username,
        }
        bad_token = jwt.encode(
            bad_token_data,
            str(cached_settings.SECRET_KEY),
            algorithm=cached_settings.ALGORITHM,
        )
        try:
            await get_active_user_by_token(bad_token)
        except HTTPException:
            assert True
        else:
            raise AssertionError("Token with no sub was sent. User should`t be received.")

    async def test_get_active_user_by_token_with_no_user(self, backend_app):
        exp_time: datetime = datetime.utcnow() + timedelta(
            minutes=cached_settings.ACCESS_TOKEN_EXPIRE_MIN
        )
        bad_token_data = {"exp": exp_time, "username": "bad-user", "sub": str(uuid4())}
        bad_token = jwt.encode(
            bad_token_data,
            str(cached_settings.SECRET_KEY),
            algorithm=cached_settings.ALGORITHM,
        )
        try:
            await get_active_user_by_token(bad_token)
        except HTTPException:
            assert True
        else:
            raise AssertionError(
                "Token with unknown user was sent. User should`t be received."
            )

    async def test_get_active_user_by_token_with_disabled_user(
        self, backend_app, single_user: UserGinoModel
    ):
        token: str = single_user.create_access_token()
        await single_user.update(disabled=True).apply()
        try:
            await get_active_user_by_token(token)
        except HTTPException:
            assert True
        else:
            raise AssertionError(
                "Token for disabled user was sent. User should`t be received."
            )


class TestAuthenticate:
    async def test_active_user(self, backend_app, single_user: UserGinoModel):
        user: UserGinoModel = await authenticate_user(
            username=single_user.username, password="test-user-password"
        )
        assert user
        assert user.id == single_user.id

    async def test_no_user(self, backend_app):
        try:
            await authenticate_user(username="fake-no-user", password="fake")
        except HTTPException:
            assert True
        else:
            raise AssertionError("There is no such user. User should`t be received.")

    async def test_bad_password(self, backend_app, single_user: UserGinoModel):
        try:
            await authenticate_user(
                username=single_user.username, password="bad-password"
            )
        except HTTPException:
            assert True
        else:
            raise AssertionError("Bad password. User should`t be received.")

    async def test_disabled_user(self, backend_app, single_disabled_user: UserGinoModel):
        try:
            await authenticate_user(
                username=single_disabled_user.username, password="test-user-password"
            )
        except HTTPException:
            assert True
        else:
            raise AssertionError("User is disabled. User should`t be received.")
