# -*- coding: utf-8 -*-
"""User core tests."""

from datetime import datetime

from asyncpg.pgproto.pgproto import UUID as UUID_PG

from core.database import UserGinoModel
from core.schemas import (
    UserDBModel,
    UserDBDataModel,
    UserDataCreateModel,
    UserDataUpdateModel,
)

import pytest

pytestmark = [
    pytest.mark.asyncio,
    pytest.mark.api_full,
    pytest.mark.auth,
    pytest.mark.security,
]


@pytest.fixture
async def user_mock():
    return {
        "ext_id": "5" * 100,
        "disabled": False,
        "superuser": False,
        "username": "user_mock",
        "given_name": "given_mock",
        "family_name": "family_mock",
        "full_name": "full_mock",
    }


@pytest.fixture
async def user_shortened_mock():
    return {"ext_id": "2" * 100, "username": "user_mock"}


@pytest.fixture
async def user_extra_mock():
    return {
        "ext_id": "1" * 100,
        "disabled": False,
        "superuser": True,
        "username": "user_mock",
        "given_name": "given_mock",
        "family_name": "family_mock",
        "full_name": "full_mock",
    }


@pytest.fixture
async def user_shortened_ser_mock(user_shortened_mock):
    return {"data": {"attributes": user_shortened_mock}}


@pytest.fixture
async def user_extra_ser_mock(user_extra_mock):
    return {"data": {"attributes": user_extra_mock}}


@pytest.fixture
async def users_1(user_extra_mock):
    return await UserGinoModel.create(**user_extra_mock)


class TestUserDB:
    """User db-table tests."""

    @pytest.mark.api_base
    async def test_user_default_create(self, api_client, user_mock):
        user_obj = await UserGinoModel.create(**user_mock)
        assert user_obj.ext_id == user_mock["ext_id"]
        assert user_obj.disabled == user_mock["disabled"]
        assert user_obj.superuser == user_mock["superuser"]
        assert user_obj.username == user_mock["username"]
        assert user_obj.given_name == user_mock["given_name"]
        assert user_obj.full_name == user_mock["full_name"]
        assert user_obj.family_name == user_mock["family_name"]
        assert isinstance(user_obj.created, datetime)
        assert isinstance(user_obj.id, UUID_PG)
        await user_obj.delete()

    @pytest.mark.api_base
    async def test_user_shortened_create(self, api_client, user_shortened_mock):
        user_obj = await UserGinoModel.create(**user_shortened_mock)
        assert user_obj.ext_id == user_shortened_mock["ext_id"]
        assert user_obj.disabled is False
        assert user_obj.superuser is False
        assert user_obj.username == user_shortened_mock["username"]
        assert user_obj.given_name is None
        assert user_obj.full_name is None
        assert user_obj.family_name is None
        assert isinstance(user_obj.created, datetime)
        assert isinstance(user_obj.id, UUID_PG)
        await user_obj.delete()

    @pytest.mark.api_base
    async def test_user_extra_create(self, api_client, user_extra_mock):
        user_obj = await UserGinoModel.create(**user_extra_mock)
        assert user_obj.ext_id == user_extra_mock["ext_id"]
        assert user_obj.disabled == user_extra_mock["disabled"]
        assert user_obj.superuser == user_extra_mock["superuser"]
        assert user_obj.username == user_extra_mock["username"]
        assert user_obj.given_name == user_extra_mock["given_name"]
        assert user_obj.full_name == user_extra_mock["full_name"]
        assert user_obj.family_name == user_extra_mock["family_name"]
        assert isinstance(user_obj.created, datetime)
        assert isinstance(user_obj.id, UUID_PG)
        await user_obj.delete()

    @pytest.mark.api_base
    async def test_user_get(self, api_client, users_1):
        assert isinstance(users_1.data["id"], UUID_PG)
        assert users_1.data["id"] == users_1.id
        assert users_1.data["type"] == "user"
        attributes = users_1.data["attributes"]
        assert isinstance(attributes["created"], datetime)
        assert attributes["created"] == users_1.created
        assert attributes["ext_id"] == users_1.ext_id
        assert attributes["family_name"] == users_1.family_name
        assert attributes["full_name"] == users_1.full_name
        assert attributes["given_name"] == users_1.given_name
        assert attributes["superuser"] == users_1.superuser
        assert attributes["username"] == users_1.username
        assert "type" not in attributes


class TestUserPydantic:
    """User pydantic serializer tests."""

    @pytest.mark.api_base
    async def test_user_serializer_get(self, api_client, users_1):
        serializer = UserDBDataModel.from_orm(users_1)
        assert isinstance(serializer, UserDBDataModel)
        assert isinstance(serializer.data, UserDBModel)
        assert serializer.data.id == users_1.id
        assert serializer.data.type == users_1.type
        assert serializer.data.attributes.ext_id == users_1.ext_id
        assert serializer.data.attributes.disabled == users_1.disabled
        assert serializer.data.attributes.superuser == users_1.superuser
        assert serializer.data.attributes.created == users_1.created
        assert serializer.data.attributes.username == users_1.username
        assert serializer.data.attributes.given_name == users_1.given_name
        assert serializer.data.attributes.family_name == users_1.family_name
        assert serializer.data.attributes.full_name == users_1.full_name

    @pytest.mark.api_base
    async def test_user_serializer_short_create(
        self, api_client, user_shortened_ser_mock
    ):
        serializer = UserDataCreateModel.parse_obj(user_shortened_ser_mock)
        assert isinstance(serializer, UserDataCreateModel)
        assert serializer.data.type == "user"
        assert (
            serializer.data.attributes.ext_id
            == user_shortened_ser_mock["data"]["attributes"]["ext_id"]  # noqa: W503
        )
        assert (
            serializer.data.attributes.username
            == user_shortened_ser_mock["data"]["attributes"]["username"]  # noqa: W503
        )
        db_obj = await UserGinoModel.create(**serializer.data.validated_attributes)
        assert db_obj.ext_id == serializer.data.attributes.ext_id
        assert db_obj.disabled is False
        assert db_obj.superuser is False
        assert db_obj.username == serializer.data.attributes.username
        assert db_obj.given_name is None
        assert db_obj.full_name is None
        assert db_obj.family_name is None
        assert isinstance(db_obj.created, datetime)
        assert isinstance(db_obj.id, UUID_PG)
        await db_obj.delete()

    @pytest.mark.api_base
    async def test_user_serializer_extra_create(self, api_client, user_extra_ser_mock):
        serializer = UserDataCreateModel.parse_obj(user_extra_ser_mock)
        assert isinstance(serializer, UserDataCreateModel)
        db_obj = await UserGinoModel.create(**serializer.data.validated_attributes)
        assert db_obj.ext_id == serializer.data.attributes.ext_id
        assert db_obj.disabled == serializer.data.attributes.disabled
        assert db_obj.superuser == serializer.data.attributes.superuser
        assert db_obj.username == serializer.data.attributes.username
        assert db_obj.given_name == serializer.data.attributes.given_name
        assert db_obj.full_name == serializer.data.attributes.full_name
        assert db_obj.family_name == serializer.data.attributes.family_name
        assert isinstance(db_obj.created, datetime)
        assert isinstance(db_obj.id, UUID_PG)
        await db_obj.delete()

    @pytest.mark.api_base
    async def test_user_serializer_update(
        self, api_client, users_1, user_shortened_ser_mock
    ):
        serializer = UserDataUpdateModel.parse_obj(user_shortened_ser_mock)
        assert isinstance(serializer, UserDataUpdateModel)
        assert serializer.data.type == "user"
        await users_1.update(**serializer.data.validated_attributes).apply()
        assert users_1.disabled is False
        assert users_1.superuser is False
