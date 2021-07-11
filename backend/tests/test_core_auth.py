# -*- coding: utf-8 -*-
"""Core auth tests."""
from datetime import datetime, timedelta
from random import randint

import pytest
from fastapi import HTTPException
from jose import jwt

from core.config import ACCESS_TOKEN_EXPIRE_MIN, ALGORITHM, GOOGLE_CLIENT_ID
from core.database import TokenInfoGinoModel, UserGinoModel
from core.schemas import GoogleIdInfo
from core.services.security import (
    get_current_user,
    get_or_create_user,
    get_user_for_refresh,
)
from core.utils.exceptions import CREDENTIALS_EX, INACTIVE_EX

pytestmark = [
    pytest.mark.asyncio,
    pytest.mark.api_full,
    pytest.mark.auth,
    pytest.mark.security,
]


@pytest.fixture
async def single_admin(api_client, user_admin_mock):
    return await UserGinoModel.create(**user_admin_mock)


@pytest.fixture
async def single_user(api_client, user_mock):
    return await UserGinoModel.create(**user_mock)


@pytest.fixture
async def single_disabled_user(api_client, disabled_user_mock):
    return await UserGinoModel.create(**disabled_user_mock)


@pytest.fixture
async def google_id_info():
    token_info = dict()
    token_info["aud"] = GOOGLE_CLIENT_ID
    token_info["exp"] = (datetime.utcnow() + timedelta(days=1)).timestamp()
    token_info["iat"] = datetime.utcnow().timestamp()
    token_info["iss"] = "accounts.google.com"
    token_info["sub"] = str(randint(1, 999)) * 84
    token_info["given_name"] = "larry"
    token_info["family_name"] = "brin"
    return GoogleIdInfo(**token_info)


@pytest.fixture
async def existing_user_id_info(google_id_info, single_admin):
    google_id_info.sub = single_admin.ext_id
    return google_id_info


@pytest.fixture
async def existing_deactivated_user_id_info(google_id_info, single_disabled_user):
    google_id_info.sub = single_disabled_user.ext_id
    return google_id_info


@pytest.fixture
async def single_admin_token(single_admin) -> dict:
    return await single_admin.create_token()


@pytest.fixture
async def token_data(single_admin) -> dict:
    return {
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MIN),
        "id": single_admin.id_str,
        "username": single_admin.username,
    }


@pytest.fixture
async def bad_token(token_data) -> dict:

    return {
        "access_token": jwt.encode(token_data, "qwe", algorithm=ALGORITHM),
        "refresh_token": jwt.encode(token_data, "qwe", algorithm=ALGORITHM),
        "token_type": "bearer",
        "alg": ALGORITHM,
        "typ": "JWT",
    }


@pytest.fixture
async def bad_access_token(bad_token) -> str:
    return bad_token["access_token"]


@pytest.fixture
async def no_refresh_token(single_admin):
    token = await TokenInfoGinoModel.get(single_admin.id)
    await token.delete()


@pytest.fixture
async def single_admin_access_token(single_admin_token) -> str:
    return single_admin_token["access_token"]


@pytest.fixture
async def single_admin_refresh_token(single_admin_token) -> str:
    return single_admin_token["refresh_token"]


@pytest.fixture
async def single_disabled_admin_token(single_admin_access_token, single_admin) -> str:
    await single_admin.update(disabled=True).apply()
    return single_admin_access_token


@pytest.fixture
async def single_disabled_refresh_token(
    single_admin_refresh_token, single_admin
) -> str:
    await single_admin.update(disabled=True).apply()
    return single_admin_refresh_token


class TestGOCUser:
    """Get or create (GOC) user tests."""

    async def test_get_or_create_user_deactivated_user(
        self, api_client, single_disabled_user, existing_deactivated_user_id_info
    ):
        try:
            await get_or_create_user(existing_deactivated_user_id_info)
        except HTTPException as ex:
            assert ex.status_code == CREDENTIALS_EX.status_code
        else:
            assert False

    async def test_get_or_create_user_update_user(
        self, api_client, single_admin, existing_user_id_info
    ):
        user_object = await get_or_create_user(existing_user_id_info)
        assert user_object.ext_id == existing_user_id_info.sub
        assert user_object.given_name == existing_user_id_info.given_name
        assert user_object.family_name == existing_user_id_info.family_name

    async def test_get_or_create_user_create_user(self, api_client, google_id_info):
        user_obj = await UserGinoModel.query.where(
            UserGinoModel.ext_id == google_id_info.sub
        ).gino.first()
        assert not user_obj
        user_object = await get_or_create_user(google_id_info)
        assert user_object.ext_id == google_id_info.sub
        assert user_object.given_name == google_id_info.given_name
        assert user_object.family_name == google_id_info.family_name


class TestGCUser:
    """Get current (GC) user tests."""

    async def test_get_current_active_user(self, api_client, single_admin_access_token):
        user_object = await get_current_user(single_admin_access_token)
        assert isinstance(user_object, UserGinoModel)

    async def test_get_current_disabled_user(
        self, api_client, single_disabled_admin_token
    ):
        try:
            await get_current_user(single_disabled_admin_token)
        except HTTPException as ex:
            assert ex.status_code == INACTIVE_EX.status_code
        else:
            assert False

    async def test_get_current_user_bad_token(self, api_client, bad_access_token):
        try:
            await get_current_user(bad_access_token)
        except HTTPException as ex:
            assert ex.status_code == CREDENTIALS_EX.status_code
        else:
            assert False

    async def test_get_current_user_no_token(self, api_client):
        try:
            await get_current_user("")
        except HTTPException as ex:
            assert ex.status_code == CREDENTIALS_EX.status_code
        else:
            assert False


class TestGUserFR:
    """Get user (GU) for refresh tests."""

    async def test_get_active_user_for_refresh(
        self, api_client, single_admin_refresh_token
    ):
        user_object = await get_user_for_refresh(single_admin_refresh_token)
        assert isinstance(user_object, UserGinoModel)

    async def test_get_disabled_user_for_refresh(
        self, api_client, single_disabled_refresh_token
    ):
        try:
            await get_user_for_refresh(single_disabled_refresh_token)
        except HTTPException as ex:
            assert ex.status_code == INACTIVE_EX.status_code
        else:
            assert False

    async def test_get_current_user_for_refresh_bad_token(
        self, api_client, bad_access_token
    ):
        try:
            await get_user_for_refresh(bad_access_token)
        except HTTPException as ex:
            assert ex.status_code == CREDENTIALS_EX.status_code
        else:
            assert False

    async def test_get_current_user_for_refresh_unknown_token(
        self, api_client, single_admin_refresh_token, no_refresh_token
    ):
        try:
            await get_user_for_refresh(single_admin_refresh_token)
        except HTTPException as ex:
            assert ex.status_code == CREDENTIALS_EX.status_code
        else:
            assert False

    async def test_get_current_user_for_refresh_no_token(self, api_client):
        try:
            await get_user_for_refresh("")
        except HTTPException as ex:
            assert ex.status_code == CREDENTIALS_EX.status_code
        else:
            assert False


# TODO: @devalv TokenInfo.save hash for refresh token

# TODO: @devalv text cases for Serializer
