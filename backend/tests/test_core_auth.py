from datetime import datetime, timedelta
from typing import Any, Dict

import pytest
import pytest_asyncio
from fastapi import status
from jose import jwt

from core import cached_settings
from core.database import TokenInfoGinoModel

pytestmark = [
    pytest.mark.asyncio,
    pytest.mark.api_full,
    pytest.mark.auth,
    pytest.mark.security,
]


API_URL_PREFIX = "/api/v2"


@pytest_asyncio.fixture
async def token_data(single_admin) -> Dict[str, Any]:
    return {
        "exp": datetime.utcnow()
        + timedelta(minutes=cached_settings.ACCESS_TOKEN_EXPIRE_MIN),
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


class TestUserInfo:
    """Authenticated user attributes tests."""

    API_URL = f"{API_URL_PREFIX}/user/info"

    async def test_granted_info(
        self, backend_app, single_admin, single_admin_auth_headers
    ):
        resp = await backend_app.get(self.API_URL, headers=single_admin_auth_headers)
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
        resp = await backend_app.get(self.API_URL)
        assert resp.status_code == status.HTTP_401_UNAUTHORIZED


async def test_refresh_access_token(backend_app, single_admin_refresh_token):
    resp = await backend_app.post(
        f"{API_URL_PREFIX}/token/refresh",
        query_string={"token": single_admin_refresh_token},
    )
    assert resp.status_code == status.HTTP_200_OK
    resp_data = resp.json()
    assert "access_token" in resp_data
    assert "refresh_token" in resp_data


async def test_refresh_access_token_with_bad_token(backend_app):
    resp = await backend_app.post(
        f"{API_URL_PREFIX}/token/refresh", query_string={"token": "qwe"}
    )
    assert resp.status_code == status.HTTP_401_UNAUTHORIZED
