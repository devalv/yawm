"""User core tests."""
from datetime import datetime

import pytest
import pytest_asyncio
from asyncpg.pgproto.pgproto import UUID as UUID_PG
from fastapi import HTTPException

from core.database import TokenInfoGinoModel, UserGinoModel
from core.schemas import UserCreateModel, UserViewModel

pytestmark = [
    pytest.mark.asyncio,
    pytest.mark.api_full,
    pytest.mark.security,
]


@pytest_asyncio.fixture
async def user_shortened_mock():
    return {"username": "user-short-mock", "password": "user-short-password"}


class TestUserDB:
    """User db-table tests."""

    @pytest.mark.api_base
    async def test_user_default_create(self, backend_app, user_mock):
        user_obj: UserGinoModel = await UserGinoModel.create(**user_mock)
        assert user_obj.disabled == user_mock["disabled"]
        assert user_obj.superuser == user_mock["superuser"]
        assert user_obj.username == user_mock["username"]
        assert isinstance(user_obj.created_at, datetime)
        if user_obj.updated_at is not None:
            assert isinstance(user_obj.updated_at, datetime)
        assert isinstance(user_obj.id, UUID_PG)
        assert user_obj.password != user_mock["password"]
        assert user_obj.verify_password(user_mock["password"])
        await user_obj.delete()

    @pytest.mark.api_base
    async def test_user_defaults_create(self, backend_app, user_shortened_mock):
        user_obj = await UserGinoModel.create(**user_shortened_mock)
        assert user_obj.disabled is False
        assert user_obj.superuser is False
        assert user_obj.username == user_shortened_mock["username"]
        assert isinstance(user_obj.created_at, datetime)
        if user_obj.updated_at is not None:
            assert isinstance(user_obj.updated_at, datetime)
        assert isinstance(user_obj.id, UUID_PG)
        assert user_obj.password != user_shortened_mock["password"]
        assert user_obj.verify_password(user_shortened_mock["password"])
        await user_obj.delete()

    @pytest.mark.api_base
    async def test_user_extra_create(self, backend_app, user_admin_mock):
        user_obj = await UserGinoModel.create(**user_admin_mock)
        assert user_obj.disabled == user_admin_mock["disabled"]
        assert user_obj.superuser == user_admin_mock["superuser"]
        assert user_obj.username == user_admin_mock["username"]
        assert isinstance(user_obj.created_at, datetime)
        assert isinstance(user_obj.created_at, datetime)
        assert isinstance(user_obj.id, UUID_PG)
        assert user_obj.password != user_admin_mock["password"]
        assert user_obj.verify_password(user_admin_mock["password"])
        await user_obj.delete()

    @pytest.mark.api_base
    async def test_user_unique_violation_create(self, backend_app, single_admin):
        try:
            user_obj = await UserGinoModel.create(
                username=single_admin.username, password="test"
            )
        except HTTPException:
            assert True
        else:
            await user_obj.delete()
            raise AssertionError("Unique violation check broken")

    @pytest.mark.api_base
    async def test_user_get(self, backend_app, single_admin):
        assert isinstance(single_admin.id, UUID_PG)
        assert isinstance(single_admin.created_at, datetime)
        if single_admin.updated_at is not None:
            assert isinstance(single_admin.updated_at, datetime)
        assert single_admin.active is True
        assert single_admin.disabled is False

    @pytest.mark.api_base
    async def test_user_get_by_username(self, backend_app, single_admin):
        user_obj: UserGinoModel = await UserGinoModel.get_by_username(
            single_admin.username
        )
        assert user_obj.id == single_admin.id


class TestUserPydantic:
    """User pydantic serializer tests."""

    @pytest.mark.api_base
    async def test_user_serializer_get(self, backend_app, single_admin):
        serializer: UserViewModel = UserViewModel.from_orm(single_admin)
        assert isinstance(serializer, UserViewModel)
        assert serializer.id == single_admin.id
        assert serializer.disabled == single_admin.disabled
        assert serializer.superuser == single_admin.superuser
        assert serializer.created_at == single_admin.created_at
        assert serializer.updated_at == single_admin.updated_at
        assert serializer.username == single_admin.username
        assert hasattr(serializer, "password") is False

    @pytest.mark.api_base
    async def test_user_serializer_short_create(self, backend_app, user_shortened_mock):
        serializer: UserCreateModel = UserCreateModel.parse_obj(user_shortened_mock)
        assert isinstance(serializer, UserCreateModel)
        assert serializer.username == user_shortened_mock["username"]
        db_obj: UserGinoModel = await UserGinoModel.create(**serializer.dict())
        assert db_obj.disabled is False
        assert db_obj.superuser is False
        assert db_obj.username == serializer.username
        assert isinstance(db_obj.created_at, datetime)
        if db_obj.updated_at is not None:
            assert isinstance(db_obj.updated_at, datetime)
        assert isinstance(db_obj.id, UUID_PG)
        assert db_obj.password != user_shortened_mock["password"]
        assert db_obj.verify_password(user_shortened_mock["password"])
        await db_obj.delete()

    @pytest.mark.api_base
    async def test_user_serializer_extra_create(self, backend_app, user_admin_mock):
        serializer: UserCreateModel = UserCreateModel.parse_obj(user_admin_mock)
        assert isinstance(serializer, UserCreateModel)
        db_obj: UserGinoModel = await UserGinoModel.create(**serializer.dict())
        assert db_obj.disabled is False
        assert db_obj.superuser is False
        assert db_obj.username == serializer.username
        assert isinstance(db_obj.created_at, datetime)
        if db_obj.updated_at is not None:
            assert isinstance(db_obj.updated_at, datetime)
        assert isinstance(db_obj.id, UUID_PG)
        assert db_obj.password != user_admin_mock["password"]
        assert db_obj.verify_password(user_admin_mock["password"])
        await db_obj.delete()


class TestUserToken:
    """User token tests."""

    async def test_create_access_token(self, backend_app, single_admin: UserGinoModel):
        access_token = single_admin.create_access_token()
        assert isinstance(access_token, str)

    async def test_create_refresh_token(self, backend_app, single_admin: UserGinoModel):
        refresh_token = await single_admin.create_refresh_token()
        assert isinstance(refresh_token, str)

    async def test_delete_refresh_token(self, backend_app, single_admin: UserGinoModel):
        await single_admin.create_token()
        token_obj: TokenInfoGinoModel = await TokenInfoGinoModel.get(single_admin.id)
        assert token_obj
        await single_admin.delete_refresh_token()
        new_token_obj: TokenInfoGinoModel = await TokenInfoGinoModel.get(single_admin.id)
        assert not new_token_obj

    async def test_create_token(self, backend_app, single_admin: UserGinoModel):
        token = await single_admin.create_token()
        assert isinstance(token, dict)

    async def test_token_info(self, backend_app, single_admin: UserGinoModel):
        await single_admin.create_token()
        token_info = await single_admin.token_info()
        assert isinstance(token_info, TokenInfoGinoModel)

    async def test_token_is_valid(self, backend_app, single_admin: UserGinoModel):
        token_is_valid = await single_admin.refresh_token_is_valid("bad")
        assert not token_is_valid
