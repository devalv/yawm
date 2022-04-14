# # -*- coding: utf-8 -*-
# """User core tests."""
# import os
# from datetime import datetime
#
# import pytest
# import pytest_asyncio
# from asyncpg.pgproto.pgproto import UUID as UUID_PG
#
# from core.database import TokenInfoGinoModel, UserGinoModel
# from core.schemas import UserCreateModel, UserViewModel
#
# pytestmark = [
#     pytest.mark.asyncio,
#     pytest.mark.api_full,
#     pytest.mark.auth,
#     pytest.mark.security,
# ]
#
#
# @pytest_asyncio.fixture
# async def user_shortened_mock():
#     return {"ext_id": "2" * 100, "username": "user_mock"}
#
#
# class TestUserDB:
#     """User db-table tests."""
#
#     @pytest.mark.api_base
#     async def test_user_default_create(self, backend_app, user_mock):
#         user_obj = await UserGinoModel.create(**user_mock)
#         assert user_obj.ext_id == user_mock["ext_id"]
#         assert user_obj.disabled == user_mock["disabled"]
#         assert user_obj.superuser == user_mock["superuser"]
#         assert user_obj.username == user_mock["username"]
#         assert user_obj.given_name == user_mock["given_name"]
#         assert user_obj.full_name == user_mock["full_name"]
#         assert user_obj.family_name == user_mock["family_name"]
#         assert isinstance(user_obj.created_at, datetime)
#         if user_obj.updated_at is not None:
#             assert isinstance(user_obj.updated_at, datetime)
#         assert isinstance(user_obj.id, UUID_PG)
#         await user_obj.delete()
#
#     @pytest.mark.api_base
#     async def test_user_shortened_create(self, backend_app, user_shortened_mock):
#         user_obj = await UserGinoModel.create(**user_shortened_mock)
#         assert user_obj.ext_id == user_shortened_mock["ext_id"]
#         assert user_obj.disabled is False
#         assert user_obj.superuser is False
#         assert user_obj.username == user_shortened_mock["username"]
#         assert user_obj.given_name is None
#         assert user_obj.full_name is None
#         assert user_obj.family_name is None
#         assert isinstance(user_obj.created_at, datetime)
#         if user_obj.updated_at is not None:
#             assert isinstance(user_obj.updated_at, datetime)
#         assert isinstance(user_obj.id, UUID_PG)
#         await user_obj.delete()
#
#     @pytest.mark.api_base
#     async def test_user_extra_create(self, backend_app, user_admin_mock):
#         user_obj = await UserGinoModel.create(**user_admin_mock)
#         assert user_obj.ext_id == user_admin_mock["ext_id"]
#         assert user_obj.disabled == user_admin_mock["disabled"]
#         assert user_obj.superuser == user_admin_mock["superuser"]
#         assert user_obj.username == user_admin_mock["username"]
#         assert user_obj.given_name == user_admin_mock["given_name"]
#         assert user_obj.full_name == user_admin_mock["full_name"]
#         assert user_obj.family_name == user_admin_mock["family_name"]
#         assert isinstance(user_obj.created_at, datetime)
#         assert isinstance(user_obj.created_at, datetime)
#         assert isinstance(user_obj.id, UUID_PG)
#         await user_obj.delete()
#
#     @pytest.mark.api_base
#     async def test_user_get(self, backend_app, single_admin):
#         assert isinstance(single_admin.id, UUID_PG)
#         assert isinstance(single_admin.created_at, datetime)
#         if single_admin.updated_at is not None:
#             assert isinstance(single_admin.updated_at, datetime)
#
#
# class TestUserPydantic:
#     """User pydantic serializer tests."""
#
#     @pytest.mark.api_base
#     async def test_user_serializer_get(self, backend_app, single_admin):
#         serializer = UserViewModel.from_orm(single_admin)
#         assert isinstance(serializer, UserViewModel)
#         assert serializer.id == single_admin.id
#         assert serializer.ext_id == single_admin.ext_id
#         assert serializer.disabled == single_admin.disabled
#         assert serializer.superuser == single_admin.superuser
#         assert serializer.created_at == single_admin.created_at
#         assert serializer.updated_at == single_admin.updated_at
#         assert serializer.username == single_admin.username
#         assert serializer.given_name == single_admin.given_name
#         assert serializer.family_name == single_admin.family_name
#         assert serializer.full_name == single_admin.full_name
#
#     @pytest.mark.api_base
#     async def test_user_serializer_short_create(self, backend_app, user_shortened_mock):
#         serializer = UserCreateModel.parse_obj(user_shortened_mock)
#         assert isinstance(serializer, UserCreateModel)
#         assert serializer.ext_id == user_shortened_mock["ext_id"]
#         assert serializer.username == user_shortened_mock["username"]
#         db_obj = await UserGinoModel.create(**serializer.dict())
#         assert db_obj.ext_id == serializer.ext_id
#         assert db_obj.disabled is False
#         assert db_obj.superuser is False
#         assert db_obj.username == serializer.username
#         assert db_obj.given_name is None
#         assert db_obj.full_name is None
#         assert db_obj.family_name is None
#         assert isinstance(db_obj.created_at, datetime)
#         if db_obj.updated_at is not None:
#             assert isinstance(db_obj.updated_at, datetime)
#         assert isinstance(db_obj.id, UUID_PG)
#         await db_obj.delete()
#
#     @pytest.mark.api_base
#     async def test_user_serializer_extra_create(self, backend_app, user_admin_mock):
#         serializer = UserCreateModel.parse_obj(user_admin_mock)
#         assert isinstance(serializer, UserCreateModel)
#         db_obj = await UserGinoModel.create(**serializer.dict())
#         assert db_obj.ext_id == serializer.ext_id
#         assert db_obj.disabled == serializer.disabled
#         assert db_obj.superuser == serializer.superuser
#         assert db_obj.username == serializer.username
#         assert db_obj.given_name == serializer.given_name
#         assert db_obj.full_name == serializer.full_name
#         assert db_obj.family_name == serializer.family_name
#         assert isinstance(db_obj.created_at, datetime)
#         if db_obj.updated_at is not None:
#             assert isinstance(db_obj.updated_at, datetime)
#         assert isinstance(db_obj.id, UUID_PG)
#         await db_obj.delete()
#
#     @pytest.mark.api_base
#     async def test_user_serializer_update(
#         self, backend_app, single_admin, user_shortened_mock
#     ):
#         serializer = UserCreateModel.parse_obj(user_shortened_mock)
#         assert isinstance(serializer, UserCreateModel)
#         await single_admin.update(**serializer.dict()).apply()
#         assert single_admin.disabled is False
#         assert single_admin.superuser is False
#
#
# @pytest.mark.skipif(
#     os.environ.get("PLATFORM") == "GITHUB", reason="Only for a local docker."
# )
# class TestUserToken:
#     """User token tests."""
#
#     async def test_create_access_token(self, backend_app, single_admin):
#         access_token = single_admin.create_access_token()
#         assert isinstance(access_token, str)
#
#     async def test_create_refresh_token(self, backend_app, single_admin):
#         refresh_token = await single_admin.create_refresh_token()
#         assert isinstance(refresh_token, str)
#
#     async def test_delete_refresh_token(self, backend_app, single_admin):
#         await single_admin.create_token()
#         token_obj = await TokenInfoGinoModel.get(single_admin.id)
#         assert token_obj
#         await single_admin.delete_refresh_token()
#         token_obj = await TokenInfoGinoModel.get(single_admin.id)
#         assert not token_obj
#
#     async def test_create_token(self, backend_app, single_admin):
#         token = await single_admin.create_token()
#         assert isinstance(token, dict)
#
#     async def test_token_info(self, backend_app, single_admin):
#         await single_admin.create_token()
#         token_info = await single_admin.token_info()
#         assert isinstance(token_info, TokenInfoGinoModel)
#
#     async def test_token_is_valid(self, backend_app, single_admin):
#         token_is_valid = await single_admin.token_is_valid("bad")
#         assert not token_is_valid
#
#     async def test_update_by_ext_id(self, backend_app, single_admin):
#         updated_user = await single_admin.insert_or_update_by_ext_id(
#             sub="1", username="updated"
#         )
#         assert single_admin.username != updated_user.username
#
#     async def test_create_by_ext_id(self, backend_app):
#         created_user = await UserGinoModel.insert_or_update_by_ext_id(
#             sub="1", username="new-user"
#         )
#         assert isinstance(created_user, UserGinoModel)
