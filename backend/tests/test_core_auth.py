# -*- coding: utf-8 -*-
"""Core auth tests."""
from datetime import datetime, timedelta
from random import randint

import pytest
from fastapi import HTTPException

from core.config import GOOGLE_CLIENT_ID
from core.database import UserGinoModel
from core.schemas import GoogleIdInfo
from core.services.security import get_or_create_user
from core.utils.exceptions import CREDENTIALS_EX

pytestmark = [
    pytest.mark.asyncio,
    pytest.mark.api_full,
    pytest.mark.auth,
    pytest.mark.security,
]


# TODO: @devalv pytest marks


@pytest.fixture
async def single_admin(api_client, user_admin_mock):
    return await UserGinoModel.create(**user_admin_mock)


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


# TODO: @devalv get_current_user
# TODO: @devalv get_user_for_refresh

# TODO: @devalv User.create_access_token
# TODO: @devalv User.create_refresh_token
# TODO: @devalv User.delete_refresh_token
# TODO: @devalv User.create_token
# TODO: @devalv User.token_info
# TODO: @devalv User.token_is_valid
# TODO: @devalv User.insert_or_update_by_ext_id
# TODO: @devalv TokenInfo.save hash for refresh token

# TODO: @devalv text cases for Serializer
